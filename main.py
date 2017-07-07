import sys
import time
import datetime
import cloudwatch
import config

cfg = config.loadConfig( sys.argv[1] )

while True:
    for device in cfg:
        print('Uploading data :{}:{}:{}:'.format(device.Location, device.Sensor, 23))
        cloudwatch.putData( device.Location, device.Sensor, 23 )
    print('Sleeping')
    time.sleep(30)
