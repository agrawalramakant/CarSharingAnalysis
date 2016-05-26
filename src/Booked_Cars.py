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
class Booked_Cars(Base):
    def __init__(self, json_file,time):
        self.Car_lic_No=json_file['vhc'][0]['lic']
        self.Location_X=json_file['loc'][0]
        self.Location_Y=json_file['loc'][0]
        temp = time.split('_')
        self.Date=int(temp[0])*10000+int(temp[1])*100+int(temp[2])
        self.Time=int(temp[3])*100+int(temp[4])
        self.Car_provider=json_file['id'][0:2]
        self.Car_id=json_file['id']
        self.Car_type=json_file['vhc'][0]['typ']
        if 'zid' in json_file:
            self.Zone_id=json_file['zid']
        else:
            self.Zone_id=0
        self.Car_model=json_file['vhc'][0]['mdl']
    
    __tablename__='Booked_Cars'
    
    record_id=Column(Integer, primary_key=True,autoincrement=True)
    Car_lic_No= Column(String)
    Location_X= Column(Float)
    Location_Y= Column(Float)
    Date =  Column(Integer)
    Time=Column(Integer)
    Car_provider	=Column(String)
    Car_id	= Column(String)
    Car_type= Column(String)
    Zone_id	= Column(Integer)
    Car_model= Column(String)
engine = database.getEngine()
print "got engine ", engine
Base.metadata.create_all(engine)
#     engine = sqal.create_engine('sqlite:///../src/Car_sharing.sqlite', echo=True)
#     session = sessionmaker()
#     s=session()
#     session.configure(bind=engine)
#     Base.metadata.create_all(engine)
    
    
    #db = Database()
    #print db , "in booked cars"
    #session = sessionmaker()
    #db.session.configure(bind=db.engine)
    #Base.metadata.create_all(db.engine)
    
    
   # def __repr__(self):
        # return "<Car_daily_data(Car_lic_No='%s', Location_X='%s', Location_Y='%s',Date='%d',Time='%s',Car_provider= '%s',Car_id='%d' , Car_type= '%s',Zone_id='%d',Car_model= '%s',)>" % (self.Car_lic_No, self.Location_X, self.Location_Y, self.Date , self.Time , self.Car_provider ,  self.Car_id , self.Car_type, self.Zone_id , self.Car_model)
         