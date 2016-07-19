'''
Created on Jul 7, 2016

@author: avinashchandra
'''
from collections import Counter
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select, and_
from sqlalchemy import create_engine

import database as db
import zone_center as zc

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

def movingPattern(start_Date,end_Date,start_Time,end_Time):
    actualStart = start_Date[0:4]+ '_'+start_Date[4:6].lstrip('0') +'_'+ start_Date[6:8].lstrip('0')\
                    + '_' + start_Time[0:2].lstrip('0') + '_' + start_Time[2:4].lstrip('0')
    actualEnd = end_Date[0:4] + '_' + end_Date[4:6].lstrip('0') + '_' + end_Date[6:8].lstrip('0') \
                  + '_' + end_Time[0:2].lstrip('0') + '_' + end_Time[2:4].lstrip('0')

