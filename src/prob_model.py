'''
Created on Jul 7, 2016

@author: avinashchandra
'''
from collections import Counter
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import select, and_
from sqlalchemy import create_engine
# engine = create_engine('sqlite:///../resource/Car_sharing_new5.sqlite', echo=False)
import database as db
#     
# def __init__(self, date,star_time,end_time):
#     
#     self.date=date
#     self.start_time=star_time
#     self.end_time=end_time
# def getEngine():
#     global engine
#     return engine
def get_analysis_info(z_Id,start_Date,end_Date = None,start_Time = None,end_Time = None):
    eng = db.getEngine()
    with eng.connect() as con:
        meta = MetaData(eng)
        cars = Table('Cars', meta, autoload=True)  
        if(start_Time is None):
            start_Time = 0
        if end_Time is None:
            end_Time = 2400
        if(end_Date is None):
            stm = select([cars]).where(and_(cars.c.b_Zone_id==z_Id,
                                   cars.c.b_Time>=start_Time,
                                   cars.c.r_Time<=end_Time,
                                   cars.c.b_Date==start_Date))
        else:
            stm = select([cars]).where(and_(cars.c.b_Zone_id==z_Id,
                                   cars.c.b_Time>=start_Time,
                                   cars.c.r_Time<=end_Time,
                                   cars.c.b_Date>=start_Date,
                                   cars.c.b_Date<=end_Date))
        rs = con.execute(stm)
        res = rs.fetchall()
        if len(res) > 0:
            return res
        else:
            return None



def get_Probability(z_Id,start_Date,end_Date = None,start_Time = None,end_Time = None):
    data=get_analysis_info(z_Id,start_Date,end_Date, start_Time,end_Time)
    r_zone_list=[]
    zone_prob={}
    for bookings in range(0,len(data)):
        r_zone_list.append(data[bookings][13])
    total_cars=float(len(r_zone_list))
    grouped_zone=Counter(r_zone_list).items()
    for zone in grouped_zone:
        zone_no=zone[0]
        prob=zone[1]/total_cars
        zone_prob[zone_no]=float(prob)
    return zone_prob
zone_prob=get_Probability(z_Id=4,start_Date=20160621,end_Date=20160629 , start_Time=1051,end_Time=1651)
print zone_prob