
def loadConfig( filename ):

    configList = []

    print('Loading configuration from file {}'.format(filename))
    file = open(filename, "r") 

    for line in file:
        tokens = line.split(",")
        x = ConfigEntry()
        x.Location = tokens[0]
        x.Sensor = tokens[1]
        x.Device = tokens[2]

        configList.append(x)

    return configList;


class ConfigEntry(object):
    pass
