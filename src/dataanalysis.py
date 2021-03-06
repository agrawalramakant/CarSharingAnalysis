'''
Created on Jul 7, 2016

@author: avinashchandra
'''
from collections import Counter
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select, and_
from sqlalchemy import create_engine

import os
import database as db
import zone_center as zc
import json

def getRecords(start_Date,end_Date = None,start_Time = None,end_Time = None,zone_id=None,carType=None):
    if zone_id is None:
        data = db.getBookingWithOutZoneID(start_Date, end_Date, start_Time, end_Time,carType)
    else:
        data=db.getBookingWithZoneID(zone_id,start_Date,end_Date, start_Time,end_Time,carType)
    return data

def getZoneProbability(zone_id,start_Date,end_Date = None,start_Time = None,end_Time = None, carType=None):
    data = getRecords(start_Date=start_Date, end_Date=end_Date,start_Time=start_Time, end_Time=end_Time, zone_id=zone_id, carType= None)
    if data is None:
        return None
    r_zone_list=[]
    zone_prob={}

    for bookings in range(0,len(data)):
        r_zone_list.append(data[bookings][13])
    total_cars=float(len(r_zone_list))
    grouped_zone=Counter(r_zone_list).items()
    for zone in grouped_zone:
        zone_no=zone[0]
        prob=round((zone[1]/total_cars),2)
        if(zone_no is not 0):
            zone_prob[zone_no]=float(prob)
    return zone_prob,data

def getMovingProbability(zone_id,start_Date,end_Date = None,start_Time = None,end_Time = None, carType=None):
    # zone_probability_dict = getZoneProbability(z_Id=4, start_Date=20160621, end_Date=20160629, start_Time=1051, end_Time=1651)
    zone_probability_dict = getZoneProbability(zone_id=zone_id, start_Date=start_Date, end_Date=end_Date, start_Time=start_Time,
                                               end_Time=end_Time, carType=carType)
    if zone_probability_dict is None:
        return None
    zone_center = zc.get_actual_zone_center(zone_probability_dict[1])
    moving_prob_dict = {}
    temp = {}
    temp['lat'] = zone_center[-1]['lat']
    temp['lng'] = zone_center[-1]['lng']
    temp['prob'] = -1
    moving_prob_dict[-1] = temp
    for k, probability in zone_probability_dict[0].items():
        temp = {}
        temp['lat'] = zone_center[k]['lat']
        temp['lng'] = zone_center[k]['lng']
        temp['prob'] = probability*100
        moving_prob_dict[k] = temp


    return moving_prob_dict

def getBookingRecords(start_Date,end_Date = None,start_Time = None,end_Time = None, carType=None):
    data = getRecords(start_Date=start_Date, end_Date=end_Date, start_Time=start_Time, end_Time=end_Time, carType=carType)
    if data is None:
        return None
    bookingLocations = []
    for entry in data:
        bookingLocations.append({'lat':entry[6],'lng':entry[7],'zid': -1})
    print (len(bookingLocations))
    return bookingLocations


def getpath(time):
    temp = time.split('_')
    path = '..'  + os.sep + 'archive' + os.sep + temp[0] + os.sep + temp[1] + os.sep + temp[2] + os.sep
    return path

def movingPattern(start_Date,end_Date,start_Time,end_Time):

    actualEnd = end_Date[0:4] + '_' + end_Date[4:6].lstrip('0') + '_' + end_Date[6:8].lstrip('0') \
                  + '_' + end_Time[0:2].lstrip('0') + '_' + end_Time[2:4].lstrip('0')


def getModifiedDateTime(date, time):
    start_hour = time[0:2].lstrip('0')
    if start_hour == u'':
        start_hour = u'0'
    start_min = time[2:4].lstrip('0')
    if start_min == u'':
        start_min = u'0'
    modifiedDateTime = date[0:4] + '_' + date[4:6].lstrip('0') + '_' + date[6:8].lstrip('0') \
                  + '_' + start_hour + '_' + start_min
    return modifiedDateTime

def getBiggerdate(src, dest):
    src = src.rstrip('.txt')
    src_list = src.split("_")

    dest = dest.rstrip('.txt')
    dest_list = dest.split("_")

    if(dest_list[4]>src_list[4]) or ((dest_list[4] == src_list[4]) and (dest_list[5]>src_list[5])):
        return True
    else:
        return False


def getAllfiles(start_Date, start_Time, end_Time, end_Date=None, carType = None):

    actualStart = getModifiedDateTime(str(start_Date),str(start_Time))
    actualEnd = getModifiedDateTime(str(end_Date), str(end_Time))
    startFile = u'datafile' + '_' +actualStart+'.txt'

    endFile =  u'datafile' + '_' +actualEnd+'.txt'

    search_dir = getpath(actualStart)

    if os.path.exists(search_dir):
        print ("exists")


        files = os.listdir(search_dir)
        filteredFiles = []
        for file in files:
            if getBiggerdate(startFile, file) and getBiggerdate(file,endFile):
                filteredFiles.append(file)

        filteredFiles = [os.path.join(os.path.abspath(search_dir), f) for f in filteredFiles]  # add path to each file
        filteredFiles = sorted(filteredFiles, key=lambda x: os.path.getmtime(x))

        if(len(filteredFiles) > 0):
            return filteredFiles
        else:
            return None
    else:
        return None

def getLatLngJson(filename, carType=None):
    outputJson = []
    with open(filename) as data_file:
        jsonData = json.load(data_file)
        for entry in list(jsonData):
            if carType is None:
                outputJson.append({'lat': entry['loc'][0], 'lng': entry['loc'][1]})
            else:
                if entry['id'].startswith(carType):
                    outputJson.append({'lat': entry['loc'][0], 'lng': entry['loc'][1]})
    return outputJson