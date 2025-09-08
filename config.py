# Load Configuration from
# a simple configuration file
def loadConfig( filename ):

    configList = []

    print('Loading configuration from file {}'.format(filename))
    file = open(filename, "r") 

    for line in file:
        tokens = line.strip().split(",")
        c = ConfigEntry()
        c.location = tokens[0]
        c.sensor = tokens[1]
        c.address = tokens[2]

        configList.append(c)

    return configList;

# Simple representation of a sensor
# read from the configuration file
class ConfigEntry(object):
    pass
