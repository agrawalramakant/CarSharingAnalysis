'''
Created on 05.05.2016

@author: r.agrawal
'''
from datacollector import DataCollector

if __name__ == '__main__':
    datacollector = DataCollector()
    data = datacollector.getCarsData()
    datacollector.writeToFile(data)
#     newData = datacollector.loadOldData('data.txt')
    datacollector.getMissingCars(data)
    
