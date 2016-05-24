# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:20:05 2016

@author: avinashchandra
"""
import sqlalchemy as sqal
from sqlalchemy.orm import sessionmaker
#import Released_Cars

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
        self.engine = sqal.create_engine('sqlite:///../resource/Car_sharing.sqlite', echo=True)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.s=self.session()

    def Add_entry(self, rel):
        
        self.s.add(rel)
        self.s.commit()