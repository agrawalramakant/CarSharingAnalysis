'''
Created on 05.05.2016

@author: r.agrawal
'''
from datacollector import DataCollector
import json
import os.path
import datetime

tempFile = "temp.txt"

def fetchAndSaveData():
    datacollector = DataCollector()
    time = datetime.datetime.now()
    data = datacollector.getCarsData()
    print data
    if(os.path.exists(tempFile)):
        missingData = json.dumps(datacollector.getMissingCars(data,tempFile))
        print missingData
    datacollector.writeToFile(data, tempFile)
#   write to data base

if __name__ == '__main__':
    
    fetchAndSaveData()
