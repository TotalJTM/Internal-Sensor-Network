import secrets
from waitress import serve
from flask import Flask, url_for, request, render_template, session, redirect
from flask_socketio import SocketIO
import globalvars as gbv
import logging
import json
import nodes as nde
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = str.encode(secrets.FLASK_KEY)

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/display/", methods=["GET"])
def sensorDataDisplay():
    return render_template('index.html')

@app.route("/display/main/", methods=["GET"])
def sensorDataDisplayMain():
	logger.debug("main display served")
	logger.debug(gbv.nodeList)
	session['passed_data'] = gbv.nodeList
	return render_template('sensordisplay.html')

@app.route('/sensorpost/<sID>/', methods=['POST'])
def sensorPost(sID):
	check = False
	rMessage = request.data
	rMessage = rMessage.decode("utf-8")
	rMessage = json.loads(rMessage)
	logger.debug(rMessage)
	if(rMessage["key"]==secrets.DEVICE_KEYS):
		for nd in gbv.nodeList:
			if(nd.nodeID == sID):
				nd.updateNodeData(rMessage)
				logger.info(f"node {sID} new message")
				pushSensorData(nd)
				check = True
		if(check == False):
			gbv.nodeList.insert(0, nde.node(sID))
			gbv.nodeList[0].updateNodeData(rMessage)
			logger.info(f"node {sID} created")
			pushNewSensor()
		return ''
	else:
		logger.info(f"node {sID} failed authentification")

def pushSensorData(nodeObj):
	logger.debug(nodeObj.toJSON())
	socketio.emit('sensor_update', nodeObj.toJSON())

def pushNewSensor():
	socketio.emit('new_sensor', "")

def startWebserver():
	serve(app, host='0.0.0.0', port=5000)
