from flask import Flask, jsonify, request
from flask_cors import CORS
import src
from multiprocessing import Pool
from src import dataanalysis as da

app = Flask(__name__)
CORS(app)

def getAttributes(args):
    startDate = args['startDate']
    endDate = args['endDate']
    startTime = args['startTime']
    endTime = args['endTime']
    carType = args['type']
    try:
        i_startDate = int(startDate)
    except:
        return None
    try:
        i_endDate = int(endDate)
    except:
        i_endDate = i_startDate
    try:
        i_startTime = int(startTime)
    except:
        i_startTime = 0
    try:
        i_endTime = int(endTime)
    except:
        i_endTime = 2400
    if carType == u'all':
        carType = None
    return (i_startDate, i_endDate, i_startTime, i_endTime, carType)

@app.route('/startDataCollection/<interval>', methods=['POST'])
def startDataCollection(interval):
    #TODO remove the comment later on
    # try:
    #     sch_interval = int(interval)
    # except:
    #     return jsonify({'res': False})
    # pool = Pool(processes=1)
    # pool.apply_async(src.startScheduledExecution,[sch_interval])
    return jsonify({'res': True})

@app.route('/stopDataCollection')
def stopDataCollection():
    pass

@app.route('/movingProbability')
def movingProbability():
    args = request.args
    attr = getAttributes(args)
    if (attr is None):
        return
    print (attr)
    zone_id = args['zid']
    ret = da.getMovingProbability(zone_id= zone_id,start_Date=attr[0], end_Date=attr[1], start_Time=attr[2], end_Time=attr[3],
                               carType=attr[4])
    return jsonify({'data':ret})


@app.route('/observedDemandHeatMap')
def observedDemandHeatMap():
    args = request.args
    attr = getAttributes(args)
    if (attr is None):
        return
    print (attr)
    ret = da.getBookingRecords(start_Date=attr[0], end_Date=attr[1], start_Time=attr[2], end_Time=attr[3],carType=attr[4])
    return jsonify({'data':ret})

@app.route('/movingPatern')
def movingPatern():
    args = request.args
    attr = getAttributes(args)
    if(attr is None):
        return
    ret = da.getBookingRecords(start_Date=attr[0], end_Date=attr[1], start_Time=attr[2], end_Time=attr[3],carType=attr[4])
    return jsonify({'data':ret})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
    # print(da.getMovingProbability(zone_id=10,start_Date=20160707,end_Date=20160707,start_Time=0,end_Time=2400))
    # da.getBookingRecords(start_Date=20160707,end_Date=20160707,start_Time=0,end_Time=2400,carType=u'dn')