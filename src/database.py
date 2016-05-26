
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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