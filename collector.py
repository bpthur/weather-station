import time
import datetime
import subprocess
import nest

def getData(sensor):
    if sensor == "onboard":
        # Raspberry Pi CPU
        try:
            temp = subprocess.Popen("vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE).stdout.read()
            # Decode bytes to string for Python 3
            temp_str = temp.decode('utf-8').strip()
            # Extract temperature value
            temp_value = temp_str.replace("temp=", "").replace("'C", "")
            return float(temp_value)
        except Exception as e:
            print("Error reading CPU temperature: {}".format(e))
            return 0.0
            
    else:
        # External Temperature Probe
        try:
            with open(sensor, 'r', encoding='utf-8') as tempfile:
                text = tempfile.read()
            
            # Parse temperature data
            tempdata = text.split("\n")[1].split(" ")[9]
            temperature = float(tempdata[2:])
            temperature = temperature / 1000
            return temperature
            
        except FileNotFoundError:
            print("Temperature sensor file not found: {}".format(sensor))
            return 0.0
        except Exception as e:
            print("Error reading temperature sensor: {}".format(e))
            return 0.0
