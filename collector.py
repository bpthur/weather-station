import time
import datetime
import cloudwatch
import subprocess

def getData(sensor):

	if(sensor == "onboard"):
		temp = subprocess.Popen("/opt/vc/bin/vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE).stdout.read()
		return float(temp.strip("temp=").replace("'C","").strip());
	else:
		print(sensor)
		return 24;

        	#tempfile = open("/sys/bus/w1/devices/28-031683b2efff/w1_slave")
        	#thetext = tempfile.read()
        	#tempfile.close()
        	#tempdata = thetext.split("\n")[1].split(" ")[9]
        	#temperature = float(tempdata[2:])
        	#inside  = temperature / 1000

	return;
