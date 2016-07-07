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
current_booking = {}
def fetchAndSaveData():
    global time_last
    global current_booking
    try:
        datacollector = DataCollector()
        time_now = getTime()
        data = datacollector.getCarsData()
        oldDataFile = getFileName(time_last)
        print time_last
        if(os.path.exists(oldDataFile)):
            missingData = datacollector.getMissingCars(data,oldDataFile)
            
            for missingEntry in missingData:
                try:   
                    db.add_entry(Cars(missingEntry, time_now))
                except:
                    print 'Booking========================================================================================='
                    traceback.print_exc()
                    print missingEntry
            releasedData = datacollector.getReleasedCars(data,oldDataFile)
            for releasedEntry in releasedData:
                try:
                    db.updateEntry(releasedEntry, time_now)
                except:
                    print '========================================================================================='
                    print("Unexpected error:", sys.exc_info()[0])
                    traceback.print_exc()
                    print releasedEntry
        datacollector.writeToFile(data, getFileName(time_now))
        time_last = time_now
    except:
        print 'exception', sys.exc_info()[0]
        traceback.print_exc()
#   write to data base
from os import listdir
if __name__ == '__main__':
#     
#     mypath = "C:\\IDP\\reconstruct data"
#     print (listdir(mypath))
    
    
    test = True
#     data = db.getLastCar('M-DX 6733')
#     print(data)
    if test:
        time_last = getTime()
        fetchAndSaveData()
        time.sleep(60)
        fetchAndSaveData()
        time.sleep(60)
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
     
