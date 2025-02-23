from tempSensor import TempSensor


class TempSensorSimulated(TempSensor):
    '''not much here, just need to be able to set the temperature'''
    def __init__(self, config):
        TempSensor.__init__(self, config.sensor_time_wait)
