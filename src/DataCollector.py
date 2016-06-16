'''
Created on 23.04.2016

@author: r.agrawal
'''
import urllib, json
from fileinput import filename
import time

class DataCollector:
    
    def getCarsData(self):
    
        data = self.readRealData()
        count = 0
        for entry in list(data['sta']):
            if(entry['prv'] == 2 or entry['prv']==3):
                #if len(entry['vhc']) > 1:
                 #   print "------------------------------------------------------------------------- ", len(entry['vhc'])
                for car in entry['vhc']:
                    count = count + 1
                    #try:
                        #print count, ' -> ' , car['id'], entry['loc'], car["lic"], " zid = ", entry['zid']
                    #except:
                    #    print ""
            else:
                data['sta'].remove(entry)
        return data['sta']

    def readRealData(self):
        print "reading data from website"
        url = "https://carsharing.mvg-mobil.de/json/stations.php"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        print "read complete"
        return data
    
    def readFromFile(self):
        with open('data.txt') as data_file:    
            data = json.load(data_file)
            return data
        
    def writeToFile(self,data):
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
            
            
    def getMissingCars(self, newData):
        oldData = self.loadOldData('data_old.txt')
        newDataList = list(newData)
        for oldEntry in list(oldData):
            if(oldEntry not in newDataList):
                with open('missing_data'+time.strftime("%Y%m%d-%H%M")+'.txt', 'w') as f:
                    json.dump(oldEntry, f)
        
    def getNewCars(self,newData):
        oldData = self.loadOldData('data_old.txt')
        newDataList = list(newData)
        oldData=list(oldData)
        for newEntry in newDataList:
            if (newEntry not in oldData):
                with open('new_cars'+time.strftime("%Y%m%d-%H%M")+'.txt', 'w') as f:
                    json.dump(newEntry, f)
         
    def loadOldData(self, filename):
        with open(filename, "r") as data_file:    
            data = json.load(data_file)
        return data