from flask import Flask, jsonify, request
from flask_cors import CORS
import src
from multiprocessing import Pool

app = Flask(__name__)
CORS(app)

@app.route('/startDataCollection/<interval>', methods=['POST'])
def startDataCollection(interval):
    try:
        sch_interval = int(interval)
    except:
        return jsonify({'res': False})
    pool = Pool(processes=1)
    pool.apply_async(src.startScheduledExecution,[sch_interval])
    return jsonify({'res': True})

@app.route('/stopDataCollection')
def stopDataCollection():
    pass

@app.route('/movingProbability')
def movingProbability():
    args = request.args
    startDate = args['startDate']
    endDate = args['endDate']
    startTime = args['startTime']
    endTime = args['endTime']
    zone_id = args['zid']
    print(startDate, endDate, startTime, endTime, zone_id)
    return jsonify({'text':startDate})

@app.route('/heatMap')
def heatMap():
    args = request.args
    startDate = args['startDate']
    endDate = args['endDate']
    startTime = args['startTime']
    endTime = args['endTime']
    print(startDate, endDate, startTime, endTime)
    return jsonify({'text':startDate})

@app.route('/getBookingPattern')
def getBookingPattern():
    args = request.args
    startDate = args['startDate']
    endDate = args['endDate']
    startTime = args['startTime']
    endTime = args['endTime']
    print(startDate, endDate, startTime, endTime)
    return jsonify({'text':startDate})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)