import time
import datetime
import cloudwatch
import subprocess
import nest

def getData(sensor):

	if(sensor == "onboard"):
		#Raspberry Pi CPU
		temp = subprocess.Popen("/opt/vc/bin/vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE).stdout.read()
		return float(temp.strip("temp=").replace("'C","").strip());
	elif(sensor.startswith('x')):
		#Nest Thremostat
		return nest.getNestTemp(sensor);
	else:
		#External Temperature Probe
        	tempfile = open(sensor)
        	text = tempfile.read()
        	tempfile.close()
        	tempdata = text.split("\n")[1].split(" ")[9]
        	temperature = float(tempdata[2:])
        	temperature  = temperature / 1000

		return temperature;
