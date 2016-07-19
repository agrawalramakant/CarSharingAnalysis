'''
Created on Jul 8, 2016

@author: avinashchandra
'''
from src.dataanalysis import get_Probability
from src.zone_center import get_zone_center
# def draw_lines(zone_Id):
desti_cord={}
source_zID=4   
probability_dict=get_Probability(z_Id=4,start_Date=20160621,end_Date=20160629 , start_Time=1051,end_Time=1651)
json_data='json_data.json'
zone_center=get_zone_center(json_data)
#     orig_zone=zone_Id
# print probability_dict
moving_prob_list = []
for k,probability in probability_dict.items():
    temp = {}
    temp['lat'] = zone_center[k]['latitude']
    temp['long'] = zone_center[k]['longitude']
    temp['prob'] = probability
    moving_prob_list.append(temp)
#     desti_cord[k]=zone_center[k]

print moving_prob_list
source_coordi=zone_center[source_zID]        
            
        