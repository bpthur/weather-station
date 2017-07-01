import time
import datetime

try:
	print "timestamp,inside,outside"

        while True:
                tempfile = open("/sys/bus/w1/devices/28-031683b2efff/w1_slave")
                thetext = tempfile.read()
                tempfile.close()
                tempdata = thetext.split("\n")[1].split(" ")[9]
                temperature = float(tempdata[2:])
                inside  = temperature / 1000
                
		tempfile2 = open("/sys/bus/w1/devices/28-051684db6bff/w1_slave")
                thetext2 = tempfile2.read()
                tempfile2.close()
                tempdata2 = thetext2.split("\n")[1].split(" ")[9]
                temperature2 = float(tempdata2[2:])
                outside = temperature2 / 1000
		
		result = str(datetime.datetime.now()) + "," + str(inside) + "," + str(outside) + "\n"
		with open("weather.log", "a") as logfile:
    			logfile.write(result)

                time.sleep(30)
except KeyboardInterrupt:
        pass


