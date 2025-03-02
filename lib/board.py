import config
import logging


log = logging.getLogger(__name__)
from tempSensorSimulated import TempSensorSimulated
from tempSensorReal import TempSensorReal
class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __str__(self):
        attributes = ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

# FIX - Board class needs to be completely removed
class Board(object):
    def __init__(self, wanted_oven):
        self.config = wanted_oven
        #print('Board', self.config)
        self.name = None
        self.active = False
        self.temp_sensor = None
        self.gpio_active = False
        self.load_libs()
        self.create_temp_sensor()
        self.temp_sensor.start()

    def load_libs(self):
        print('Loading thermocouple_type', self.config.thermocouple_type)
        return
        if config.max31855:
            try:
                #from max31855 import MAX31855, MAX31855Error
                self.name='MAX31855'
                self.active = True
                log.info("import %s " % (self.name))
            except ImportError:
                msg = "max31855 config set, but import failed"
                log.warning(msg)

        if config.max31856:
            try:
                #from max31856 import MAX31856, MAX31856Error
                self.name='MAX31856'
                self.active = True
                log.info("import %s " % (self.name))
            except ImportError:
                msg = "max31856 config set, but import failed"
                log.warning(msg)

    def create_temp_sensor(self):
        if self.config.simulate == 1:
            self.temp_sensor = TempSensorSimulated()
        else:
            self.temp_sensor = TempSensorReal(self.config)

