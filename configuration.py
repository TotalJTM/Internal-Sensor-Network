import json
import nodes as nde
import globalvars as gbv

configurationFileDir = "config/"
class configuration():

	def __init__(self):
		gbv.nodeList = []
		newlist = []
		with open(configurationFileDir+'nodesensorlist.json') as file:
			d = json.load(file)
			for i in d["nodes"]:
				print(i)
				gbv.nodeList.insert(0,nde.node(i["nodeID"],i["nodeAssignedName"], i["batteryType"]))
				for s in i["sensors"]:
					ss = gbv.nodeList[0].sensor(s["sensorID"], s["sensorType"], s["sensorAssignedName"], s["sensorCalibration"])
					gbv.nodeList[0].sensors.insert(-1, ss)