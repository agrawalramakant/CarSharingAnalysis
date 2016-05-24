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




def getFileName( time):
    path = '..' + os.sep + 'archive' +os.sep
    return path + 'datafile' + '_' + time + '.txt'

def getTime():
    time = datetime.now()
    return str(time.year) + '_' + str(time.month) + '_' + str(time.day) + '_' + str(time.hour) + '_' + str(time.minute)

time_last = getTime()

def fetchAndSaveData():
    global time_last
    print 'fetcher called'
    try:
        datacollector = DataCollector()
        time_now = getTime()
        data = datacollector.getCarsData()
        oldDataFile = getFileName(time_last)
        print time_last
        if(os.path.exists(oldDataFile)):
            missingData = json.dumps(datacollector.getMissingCars(data,oldDataFile))
            print missingData
        datacollector.writeToFile(data, getFileName(time_now))
        time_last = time_now
    except:
        print 'exception', sys.exc_info()[0]
#   write to data base

if __name__ == '__main__':
#     time_last = getTime()
#     fetchAndSaveData()
#     time.sleep(120)
#     fetchAndSaveData()
    scheduler = GeventScheduler()
    scheduler.add_job(fetchAndSaveData, 'interval', minutes=2)
    g = scheduler.start()  # g is the greenlet that runs the scheduler loop
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
 
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass
    
