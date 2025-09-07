#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mqtt_client.py
import paho.mqtt.client as mqtt
import json
import datetime
import time

class MQTTClient:
    def __init__(self, broker_host, broker_port=1883, username=None, password=None, client_id="weather-station"):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client(client_id=client_id)
        
        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        
        # Set credentials if provided
        if username and password:
            self.client.username_pw_set(username, password)
        
        # Connect to broker
        try:
            self.client.connect(broker_host, broker_port, 60)
            self.client.loop_start()
            print("Connected to MQTT broker at {}:{}".format(broker_host, broker_port))
        except Exception as e:
            print("Failed to connect to MQTT broker: {}".format(e))
            raise
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("MQTT Client connected successfully")
        else:
            print("Failed to connect to MQTT broker, return code {}".format(rc))
    
    def on_disconnect(self, client, userdata, rc):
        print("MQTT Client disconnected with result code {}".format(rc))
    
    def on_publish(self, client, userdata, mid):
        print("Message published with mid: {}".format(mid))
    
    def putData(self, location, sensor, reading):
        try:
            # Create clean topic name
            clean_location = location.lower().replace(' ', '_').replace('-', '_')
            clean_sensor = sensor.lower().replace(' ', '_').replace('-', '_')
            
            # Topic for raw sensor data
            topic = "weather-station/{}/{}".format(clean_location, clean_sensor)
            
            # Payload with metadata
            payload = {
                "value": float(reading),
                "timestamp": datetime.datetime.now().isoformat(),
                "location": location,
                "sensor": sensor,
                "unit": "°C"
            }
            
            # Publish the data
            result = self.client.publish(topic, json.dumps(payload), qos=1, retain=True)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print("Successfully published to {}".format(topic))
                
                # Also publish Home Assistant auto-discovery config (one-time setup)
                self.publish_ha_discovery(clean_location, clean_sensor, location, sensor)
                return True
            else:
                print("Failed to publish to MQTT: {}".format(result.rc))
                return False
                
        except Exception as e:
            print("Error publishing to MQTT: {}".format(e))
            return False
    
    def publish_ha_discovery(self, clean_location, clean_sensor, location, sensor):
        """Publish Home Assistant MQTT Discovery configuration"""
        
        # Create unique entity ID
        entity_id = "{}_{}".format(clean_location, clean_sensor)
        
        # Discovery topic
        discovery_topic = "homeassistant/sensor/{}/config".format(entity_id)
        
        # Configuration payload for Home Assistant
        config_payload = {
            "name": "{} {}".format(location, sensor),
            "unique_id": "weather_station_{}".format(entity_id),
            "state_topic": "weather-station/{}/{}".format(clean_location, clean_sensor),
            "value_template": "{{ value_json.value }}",
            "unit_of_measurement": "°C",
            "device_class": "temperature",
            "state_class": "measurement",
            "json_attributes_topic": "weather-station/{}/{}".format(clean_location, clean_sensor),
            "device": {
                "identifiers": ["weather_station_{}".format(clean_location)],
                "name": "Weather Station {}".format(location),
                "model": "Raspberry Pi Weather Station",
                "manufacturer": "DIY"
            }
        }
        
        # Publish discovery config (retained)
        self.client.publish(discovery_topic, json.dumps(config_payload), qos=1, retain=True)
    
    def disconnect(self):
        """Clean disconnect from MQTT broker"""
        self.client.loop_stop()
        self.client.disconnect()
