# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:35:27 2016

@author: avinashchandra
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
# import DB_Entry as db

import database
global Base 
Base = declarative_base()
class Cars(Base):
    def __init__(self, json_file,b_time):

        self.Car_lic_No=json_file['vhc'][0]['lic']
        self.Car_provider=json_file['id'][0:2]
        self.Car_id=json_file['id']
        self.Car_type=json_file['vhc'][0]['typ']
        self.Car_model=json_file['vhc'][0]['mdl']
        self.b_Location_X=json_file['loc'][0]
        self.b_Location_Y=json_file['loc'][1]
        if 'zid' in json_file:
            self.b_Zone_id=json_file['zid']
        else:
            self.b_Zone_id=0
        temp = b_time.split('_')
        self.b_Date=int(temp[0])*10000+int(temp[1])*100+int(temp[2])
        self.b_Time=int(temp[3])*100+int(temp[4])
#         
        
    __tablename__='Cars'
    
    record_id=Column(Integer, primary_key=True,autoincrement=True)
    Car_lic_No= Column(String)
    Car_provider	=Column(String)
    Car_id	= Column(String)
    Car_type= Column(String)
    Car_model= Column(String)
    b_Location_X= Column(Float)
    b_Location_Y= Column(Float)
    b_Zone_id    = Column(Integer)
    b_Date =  Column(Integer)
    b_Time=Column(Integer)
    r_Time=Column(Integer)
    r_Date =  Column(Integer)
    r_Zone_id    = Column(Integer)
    r_Location_X= Column(Float)
    r_Location_Y= Column(Float)
    
   
        
engine = database.getEngine()
print "got engine ", engine
Base.metadata.create_all(engine)
 