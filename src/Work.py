# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:09:18 2016

@author: avinashchandra
"""

from Booked_Cars import Booked_Cars 
#import Released_Cars
from DB_Entry import DB_Entry
import json

#def __init__(self):

with open ("Sample_data.json", "r") as f:
    data = json.load(f) 
#json_data1=open("Sample_data.json").read()
#json_file=json.loads(json_data1)
t=Booked_Cars(data,'16_05_19_16_20')
ab = DB_Entry()
ab.Add_entry(t)
