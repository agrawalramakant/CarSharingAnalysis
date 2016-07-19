
from sqlalchemy import MetaData, Table, update
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, and_
import logging
import os
from datetime import datetime
from sqlalchemy.sql.expression import desc

Base = declarative_base()
time = datetime.now()
db_log_file_name =  '..'+os.sep+'db'+str(time.year) + '_' + str(time.month) + '_' + str(time.day) + '_' + str(time.hour)  +'.log'
print db_log_file_name
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///resource/Car_sharing_db.sqlite', echo=False)
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)


def getEngine():
    global engine
    return engine

def getsession():
    global session
    s = session()
    return s

def add_entry(obj):
    s = getsession()
    s.add(obj)
    s.commit()
    
def updateEntry(json_file, r_time):
    eng = getEngine()
    with eng.connect() as con:
        meta = MetaData(eng)
        cars = Table('Cars', meta, autoload=True)
        stm = select([cars]).where(cars.c.Car_lic_No.like(json_file['vhc'][0]['lic'])).order_by(desc(cars.c.record_id)).limit(1)
        rs = con.execute(stm)
        result = rs.fetchall() 
        if(len(result)>0):
            entry = result[0]
            z_id = 0
            if 'zid' in json_file:
                z_id=json_file['zid']
            temp = r_time.split('_')
            date = int(temp[0])*10000+int(temp[1])*100+int(temp[2])
            time = int(temp[3])*100+int(temp[4])
            if ((int(date) > int(entry[9]) or int(time) > int(entry[10])) and (int(date)<= int(entry[9])+1)):
                u= update(cars).where(cars.c.record_id==entry[0]).values(r_Location_X=json_file['loc'][0],r_Location_Y = json_file['loc'][1],r_Zone_id = z_id,r_Date = date, r_Time = time)
                con.execute(u)
        
    
def getLastCar(lic_no):
    eng = getEngine()
    with eng.connect() as con:
        meta = MetaData(eng)
        cars = Table('Cars', meta, autoload=True)  
    
        stm = select([cars]).where(cars.c.Car_lic_No.like(lic_no)).order_by(desc(cars.c.record_id)).limit(1)
        rs = con.execute(stm)
        res = rs.fetchall()
        if len(res) > 0:
            return res[0]
        else:
            return None

def getLast():
    eng = getEngine()
    with eng.connect() as con:
        meta = MetaData(eng)
        cars = Table('Cars', meta, autoload=True)  
    
        stm = select([cars]).order_by(desc(cars.c.record_id)).limit(1)
        rs = con.execute(stm)
        return rs.fetchall()[0]

def getBookingWithZoneID(z_Id,start_Date,end_Date = None,start_Time = None,end_Time = None,carType=None):
    eng = getEngine()
    with eng.connect() as con:
        meta = MetaData(eng)
        cars = Table('Cars', meta, autoload=True)
        if(carType is None):
            stm = select([cars]).where(and_(cars.c.b_Zone_id==z_Id,
                                   cars.c.b_Time>=start_Time,
                                   cars.c.r_Time<=end_Time,
                                    cars.c.b_Date >= start_Date,
                                    cars.c.b_Date <= end_Date))
        else:
            stm = select([cars]).where(and_(cars.c.b_Zone_id==z_Id,
                                   cars.c.b_Time>=start_Time,
                                   cars.c.r_Time<=end_Time,
                                   cars.c.b_Date>=start_Date,
                                   cars.c.b_Date<=end_Date),
                                       cars.c.Car_provider==carType)
        rs = con.execute(stm)
        res = rs.fetchall()
        if len(res) > 0:
            return res
        else:
            return None

def getBookingWithOutZoneID(start_Date,end_Date = None,start_Time = None,end_Time = None, carType=None):
    eng = getEngine()
    with eng.connect() as con:
        meta = MetaData(eng)
        cars = Table('Cars', meta, autoload=True)
        if(carType is None):
            stm = select([cars]).where(and_(
                                   cars.c.b_Time>=start_Time,
                                   cars.c.r_Time<=end_Time,
                                   cars.c.b_Date >= start_Date,
                                   cars.c.b_Date <= end_Date))
        else:
            stm = select([cars]).where(and_(
                                   cars.c.b_Time>=start_Time,
                                   cars.c.r_Time<=end_Time,
                                   cars.c.b_Date>=start_Date,
                                   cars.c.b_Date<=end_Date,
                                   cars.c.Car_provider==carType))
        rs = con.execute(stm)
        res = rs.fetchall()
        if len(res) > 0:
            return res
        else:
            return None