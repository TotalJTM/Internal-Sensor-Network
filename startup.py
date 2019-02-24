import webserver as server
import nodes as nde
import globalvars as gbv
import secrets
from threading import Thread 
from threading import active_count
import sys
import logging
import os, time
from configuration import configuration
logger = logging.getLogger(__name__)

def increaseBatt():
	for j in range(0,10):
		gbv.nodeList[0].batteryReadings.insert(0,j)
		logger.info(f"batt {j}")
		server.pushSensorData(gbv.nodeList[0])
		time.sleep(1)

def main():
	#start server files
	gbv.init()

	logger.debug('server started')
	confManager = configuration()
	#t = Thread(target=increaseBatt)
	#t.daemon = True
	#t.start()
	flaskThread = Thread(target=server.startWebserver)
	flaskThread.daemon = True
	flaskThread.start()

	while active_count() > 0:
		time.sleep(0.1)
	#serve(server.app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
	cwd = os.getcwd()
	logging.basicConfig(level=logging.DEBUG) #filename=f'{cwd}/logs/mainlog.log', 
	main()