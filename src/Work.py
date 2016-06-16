# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:09:18 2016

@author: avinashchandra
"""

from Booked_Cars import Booked_Cars 
#import Released_Cars
#from DB_Entry import DB_Entry
#import json
import yaml
import json


with open ("temp.txt", "r") as f:
    data = json.load(f) 
list = list(data)
t=Booked_Cars(list[3],'2016_05_19_16_20')
#ab = DB_Entry()
#ab.Add_entry(t)
