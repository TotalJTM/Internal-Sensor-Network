import time, json
import logging
import globalvars as gbv
logger = logging.getLogger(__name__)

class node():
	def __init__(self, eid, ename="", nDataLength=5, ebattReadType=0):
		self.nodeName = ename					#name we give the node
		self.nodeID	= eid						#name the node has assigned itself
		self.batteryReadingType = ebattReadType
		self.batteryReadings = []				#array of recent battery voltages
		self.lastResponse = []					#array of time values, when sensor responds add a new list item
		self.sensors = []						#sensors attached to our node
		self.nodeDataLength = nDataLength 		#amount of battery and response readings by system
		logger.debug(f"new node created [{self.nodeName}]")
	class sensor():
		def __init__(self, esid, eType, ename="", sdataLength=5, esCal=""):
			self.sensorName = ename						#name of sensor (dafults to nothing)
			self.sensorType = eType						#type of sensor
			self.sensorID = esid						#id of sensor given by device
			self.sensorData = []						#recent data for sensor device
			self.sensorCalibration = esCal
			self.sensorDataLength = sdataLength 		#amount of data to be held by system
		
		def updateSensorData(self, newData):			#update a specific sensor's data
			if(len(self.sensorData)>=self.sensorDataLength):
				self.sensorData.pop(-1)
				self.sensorData.insert(0, newData)
			else:
				self.sensorData.insert(0, newData)

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def updateNodeData(self, emessageJSON):							#update a specific node's data
		status = False
		rjson = emessageJSON #json.load(emessageJSON)
		for jsonObj in rjson["sensors"]:
			for i in self.sensors:
				if(jsonObj['id'] == i.sensorID):
					i.updateSensorData(jsonObj['data'])
					status = True
			if(status == False):
				self.sensors.insert(len(self.sensors),self.sensor(jsonObj['id'],jsonObj['type']))
				self.sensors[-1].updateSensorData(jsonObj['data'])

		if(len(self.batteryReadings)>=self.nodeDataLength):
			self.batteryReadings.pop(-1)
			self.batteryReadings.insert(0, rjson['battery'])
			self.lastResponse.pop(-1)
			self.lastResponse.insert(0, time.strftime("%d:%H:%M:%S", time.localtime()))
		else:
			self.batteryReadings.insert(0, rjson['battery'])
			self.lastResponse.insert(0, time.strftime("%d:%H:%M:%S", time.localtime()))