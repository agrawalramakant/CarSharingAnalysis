# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:20:05 2016

@author: avinashchandra
"""
import sqlalchemy as sqal
from sqlalchemy.orm import sessionmaker
#import Released_Cars
import logging

def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance

@singleton
class DB_Entry():

    def __init__(self):
#         import logging

#         active_db_url = 'postgres://lad_test:lad_test@192.168.62.173/lad_test'
        
        db_log_file_name = 'db.log'
        db_handler_log_level = logging.INFO
        db_logger_log_level = logging.DEBUG
        
        db_handler = logging.FileHandler(db_log_file_name)
        db_handler.setLevel(db_handler_log_level)
        
        db_logger = logging.getLogger('sqlalchemy')
        db_logger.addHandler(db_handler)
        db_logger.setLevel(db_logger_log_level)
        
#         engine = sqal.create_engine(active_db_url, echo=False)
        
        self.engine = sqal.create_engine('sqlite:///../resource/Car_sharing.sqlite', echo=False)
        self.engine.connect()
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.s=self.session()

    def Add_entry(self, rel):
        
        self.s.add(rel)
        self.s.commit()