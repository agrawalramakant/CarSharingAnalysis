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
        print "writing to file done"
            
    def getMissingCars(self, newData, tempFile):
        missingCars = []
        oldData = self.loadOldData(tempFile)
        newDataList = list(newData)
        for entry in newDataList:
            try:
                entry['vhc']
            except:
                newDataList.remove(entry)
        testCars = []
        for oldEntry in list(oldData):
            try:
#                 if(not any(entry['vhc'][0]['lic'] == oldEntry['vhc'][0]['lic'] for entry in newDataList)):
#                     testCars.append(oldEntry)
#                 if(oldEntry not in newDataList):
#                     testCars.append(oldEntry)
                isPresent = False
                for entry in newDataList:
                    if( entry['vhc'][0]['lic'] == oldEntry['vhc'][0]['lic']):
                        isPresent = True
                        break
                if(not isPresent):
                    missingCars.append(oldEntry)
            except:
                print(oldEntry)
#         print "no of mssing cars in any logic", len(testCars)
        print "no of entry in missing cars : ", len(missingCars)    
        return missingCars
        
    def getReleasedCars(self, newData, tempFile):
        releasedCars = []
        oldData = self.loadOldData(tempFile)
        oldDataList = list(oldData)
        for entry in oldDataList:
            try:
                entry['vhc']
            except:
                oldDataList.remove(entry)
        testCars= []
        for newEntry in list(newData):
            try:
                if(not any(entry['vhc'][0]['lic'] == newEntry['vhc'][0]['lic'] for entry in oldDataList)):
                    testCars.append(newEntry)
                isPresent = False
                for entry in oldDataList:
                    if( entry['vhc'][0]['lic'] == newEntry['vhc'][0]['lic']):
                        isPresent = True
                        break
                if(not isPresent):
                    releasedCars.append(newEntry)
            except:
                print(newEntry)
        print "no of relased car with any logic:", len(testCars)
        print "no of entry in released cars : ", len(releasedCars)    
        return releasedCars
    
    def loadOldData(self, filename):
        with open(filename) as data_file:    
            data = json.load(data_file)
        return data
