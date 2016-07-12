'''
Created on Jul 7, 2016

@author: avinashchandra
'''
# -*- coding: utf-8 -*-

import json

coordinates={}
counter = {}
def get_zone_center(json_data):
    
    zid_range = 0   
    with open(json_data) as json_data:
        json_file=json.load(json_data)
#         d=len(json_file["sta"])
#         points = {"latitude": 0, "longitude": 0}
        for entry in json_file["sta"]:
            if 'zid' in entry:
    #             for x in range(1,33):
    #                 if entry['zid']==x:
                x = entry['zid']
                try:
                    coordinates[x]["latitude"]
                except:
                    coordinates.setdefault(x,{"latitude": 0, "longitude": 0})
    #             if coordinates[x]["latitude"] is None:
    #                 coordinates[x]["latitude"] = entry["loc"][0] 
    #             else:
                coordinates[x]["latitude"] += entry["loc"][0]
    #             if coordinates[x]["longitude"] is None:
    #                 coordinates[x]["longitude"] = entry["loc"][1]        
    #             else:
                coordinates[x]["longitude"] += entry["loc"][1]
                try:
                    counter[x] += 1
                except:
                    counter[x] = 1
                if(x > zid_range):
                    zid_range = x
                        
    for x in range(1,zid_range):
        try:
            #normal coordinates has value till 5 decimal places.
            coordinates[x]["longitude"] = round((coordinates[x]["longitude"]/counter[x]),5)
            coordinates[x]["latitude"] = round((coordinates[x]["latitude"]/counter[x]),5)
        except:
            pass
                         
    return(coordinates)
# json_data='json_data.json'
# cordi=get_zone_center(json_data)
# print cordi


        
