
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import logging
import os
from datetime import datetime

Base = declarative_base()
time = datetime.now()
db_log_file_name = '..'+os.sep+ '..'+os.sep+'db'+str(time.year) + '_' + str(time.month) + '_' + str(time.day) + '_' + str(time.hour)  +'.log'
print db_log_file_name
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///../resource/Car_sharing.sqlite', echo=False)
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