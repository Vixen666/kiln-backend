from tempSensorSimulated import TempSensorSimulated

class BoardSimulated(object):
    def __init__(self, config):
        print("BoardSimulated")
        self.temp_sensor = TempSensorSimulated(config)