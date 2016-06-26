'''
Created on 05.05.2016

@author: r.agrawal
'''
from datacollector import DataCollector
import json
import os
import sys
from datetime import datetime
import time
from apscheduler.schedulers.gevent import GeventScheduler
from Cars import Cars
import database as db
import traceback




def getFileName( time):
    temp = time.split('_')
    path = '..' + os.sep + '..' + os.sep + 'archive' + os.sep + temp[0] + os.sep + temp[1] + os.sep + temp[2] + os.sep
    # if the path does not exists then create the path
    if(not os.path.exists(path)):
        os.makedirs(path)
    return path + 'datafile' + '_' + time + '.txt'

def getTime():
    time = datetime.now()
    return str(time.year) + '_' + str(time.month) + '_' + str(time.day) + '_' + str(time.hour) + '_' + str(time.minute)

time_last = getTime()

def fetchAndSaveData():
    global time_last
    try:
        datacollector = DataCollector()
        time_now = getTime()
        data = datacollector.getCarsData()
        oldDataFile = getFileName(time_last)
#         data = datacollector.readFromFile()
#         oldDataFile = "../archive/datafile_2016_5_24_9_7.txt"
        print time_last
        if(os.path.exists(oldDataFile)):
            missingData = datacollector.getMissingCars(data,oldDataFile)
            
            for missingEntry in missingData:
                try:
                    db.add_entry(Cars(missingEntry, time_now, 'B'))
                except:
                    print '========================================================================================='
#                     print("Unexpected error:", sys.exc_info()[0])
                    traceback.print_exc()
                    print missingEntry
            releasedData = datacollector.getReleasedCars(data,oldDataFile)
            for releasedEntry in releasedData:
                try:
                    db.add_entry(Cars(releasedEntry, time_now, 'R'))
                except:
                    print '========================================================================================='
                    print("Unexpected error:", sys.exc_info()[0])
                    print releasedEntry
        datacollector.writeToFile(data, getFileName(time_now))
        time_last = time_now
    except:
        print 'exception', sys.exc_info()[0]
        traceback.print_exc()
#   write to data base

if __name__ == '__main__':
    
    test = False
    if test:
        time_last = getTime()
        fetchAndSaveData()
        time.sleep(30)
        fetchAndSaveData()
        time.sleep(30)
        fetchAndSaveData()
    else:
        scheduler = GeventScheduler()
        fetchAndSaveData()
        scheduler.add_job(fetchAndSaveData, 'interval', minutes=5)
        g = scheduler.start()  # g is the greenlet that runs the scheduler loop
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        
        # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
        try:
            g.join()
        except (KeyboardInterrupt, SystemExit):
            pass
     
