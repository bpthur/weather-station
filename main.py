import sys
import time
import datetime
import config
import collector
import mqtt_client

# Load configuration
cfg = config.loadConfig(sys.argv[1])

# Initialize MQTT client
# Update these settings for your MQTT broker
MQTT_BROKER_HOST = "192.168.1.138"  # e.g., "192.168.1.100" or "localhost"
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = None  # Set if your broker requires auth
MQTT_PASSWORD = None  # Set if your broker requires auth

try:
    mqtt = mqtt_client.MQTTClient(
        broker_host=MQTT_BROKER_HOST,
        broker_port=MQTT_BROKER_PORT,
        username=MQTT_USERNAME,
        password=MQTT_PASSWORD
    )
    
    while True:
        for device in cfg:
            try:
                print('Acquiring data :{}:{}:'.format(device.location, device.sensor))
                reading = collector.getData(device.address)

                print('Persisting data :{}:{}:{}'.format(device.location, device.sensor, reading))
                
                # Send to MQTT
                success = mqtt.putData(device.location, device.sensor, reading)
                if not success:
                    print("Failed to send data to MQTT")
                    
            except Exception as e:
                print('Unexpected Error acquiring/sending data: {}'.format(e))

        print('Sleeping')
        time.sleep(30)
        
except KeyboardInterrupt:
    print("Shutting down...")
    mqtt.disconnect()
    sys.exit(0)
except Exception as e:
    print("Fatal error: {}".format(e))
    sys.exit(1)
