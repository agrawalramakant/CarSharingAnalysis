'''
Created on Jul 7, 2016

@author: avinashchandra
'''
# -*- coding: utf-8 -*-

import json

def get_actual_zone_center(entries):
    #13,14,15
    entry_counter=0
    coordinates = {}
    counter = {}
    zid_range = 0
    for entry in entries:
        if entry[13]:
            x = entry[13]
            coordinates.setdefault(-1, {"lat": 0, "lng": 0})
            try:
                coordinates[x]["lat"]
            except:
                coordinates.setdefault(x,{"lat": 0, "lng": 0})
            coordinates[x]["lat"] += entry[14]
            coordinates[x]["lng"] += entry[15]
            coordinates[-1]["lat"] += entry[6]
            coordinates[-1]["lng"] += entry[7]
            try:
                counter[x] += 1
            except:
                counter[x] = 1
            if(x > zid_range):
                zid_range = x
            entry_counter+=1
        else:    
            print "i m in else", entry
                        
    for x in range(1,zid_range+1):
        try:
            #normal coordinates has value till 5 decimal places.
            coordinates[x]["lng"] = round((coordinates[x]["lng"]/counter[x]),5)
            coordinates[x]["lat"] = round((coordinates[x]["lat"]/counter[x]),5)
        except:
            pass
    try:
        coordinates[-1]["lng"] = round((coordinates[-1]["lng"] / entry_counter), 5)
        coordinates[-1]["lat"] = round((coordinates[-1]["lat"] / entry_counter), 5)
    except:
        pass
                         
    return(coordinates)



        
