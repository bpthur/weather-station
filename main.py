import sys
import time
import datetime
import cloudwatch
import config
import collector

cfg = config.loadConfig( sys.argv[1] )

while True:
    for device in cfg:
	
	#Acquire
        print('Acquiring data :{}:{}:'.format(device.location, device.sensor))
        reading = collector.getData(device.location, device.sensor)

	#Persist
        print('Persisting data :{}:{}:{}'.format(device.location, device.sensor, reading))
        cloudwatch.putData( device.location, device.sensor, reading )

    print('Sleeping')
    time.sleep(30)
