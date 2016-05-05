'''
Created on 23.04.2016

@author: r.agrawal
'''
import urllib, json
from crontab import *

def callMe():
    print "function called"
def main():
    print 'main'
    #init cron
    
    data = readRealData()
#     data = readFromFile()
    count = 0
    
#     for i in xrange(len(data['sta'])):
#         if(data['sta'][i]['prv']!= 2 and data['sta'][i]['prv']!= 3):
#             data['sta'].pop(i)
            
    for entry in list(data['sta']):
        if(entry['prv'] == 2 or entry['prv']==3):
            print len(entry['vhc'])
            for car in entry['vhc']:
                count = count + 1
                try:
                    print count, ' -> ' , car['id'], entry['loc'], car["lic"], " zid = ", entry['zid']
                except:
                    print ""
        else:
            data['sta'].remove(entry)
    writeToFile(data)

def readRealData():
    url = "https://carsharing.mvg-mobil.de/json/stations.php"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data

def readFromFile():
    with open('data.txt') as data_file:    
        data = json.load(data_file)
        return data
    
def writeToFile(data):
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    main()
#     cron   = CronTab()
#     job  = cron.new(command='python test.py')
#     job.minute.every(1)