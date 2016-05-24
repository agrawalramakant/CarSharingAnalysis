'''
Created on 23.04.2016

@author: r.agrawal
'''
import urllib, json

class DataCollector(object):
    
    def __init__(self):
        self.sourceUrl = "https://carsharing.mvg-mobil.de/json/stations.php"

    def getCarsData(self):
    
        data = self.readRealData()
        for entry in list(data['sta']):
            if(entry['prv'] != 2 and entry['prv'] !=3):
                data['sta'].remove(entry)
        return data['sta']

    def readRealData(self):
        response = urllib.urlopen(self.sourceUrl)
        data = json.loads(response.read())
        return data
    
    def readFromFile(self):
        with open('data.txt') as data_file:    
            data = json.load(data_file)
            return data
        
    def writeToFile(self,data,tempFile):
        with open(tempFile, 'w') as outfile:
            json.dump(data, outfile)
        print "writing to file done", tempFile
            
    def getMissingCars(self, newData, tempFile):
        missingCars = []
        oldData = self.loadOldData(tempFile)
        newDataList = list(newData)
        for oldEntry in list(oldData):
            if(oldEntry not in newDataList):
                missingCars.append(oldEntry)
        print "no of entry in missing cars : ", len(missingCars)    
        return missingCars
        
        
    def loadOldData(self, filename):
        with open(filename) as data_file:    
            data = json.load(data_file)
        return data
