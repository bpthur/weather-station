import sys
import time
import datetime
import cloudwatch
import config
import collector

cfg = config.loadConfig( sys.argv[1] )

while True:
    for device in cfg:
	try:	
		#Acquire
        	print('Acquiring data :{}:{}:'.format(device.location, device.sensor))
        	reading = collector.getData(device.address)

		#Persist
        	print('Persisting data :{}:{}:{}'.format(device.location, device.sensor, reading))
        	cloudwatch.putData( device.location, device.sensor, reading )
	except:
		print('Unexpected Error:', sys.exc_info()[0])

    print('Sleeping')
    time.sleep(30)
