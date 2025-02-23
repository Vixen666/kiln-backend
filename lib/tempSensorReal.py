import threading
import time
import random
import datetime
import logging
import json
import config
import os
import Adafruit_DHT
import glob

from boardSimulated import BoardSimulated
from tempSensor import TempSensor
log = logging.getLogger(__name__)

class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __str__(self):
        attributes = ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

class TempSensorReal(TempSensor):
    '''real temperature sensor thread that takes N measurements
       during the time_step'''
    def __init__(self, wanted_oven):
        self.config = wanted_oven
        print('TempSensorReal', self.config)

        TempSensor.__init__(self, self.config.sensor_time_wait)
        self.sleeptime = self.time_step / float(self.config.temperature_average_samples)
        self.bad_count = 0
        self.ok_count = 0
        self.bad_stamp = 0
        self.config.thermocouple_type = 'DHT11';
        config.gpio_sensor_cs = 12;
        config.gpio_sensor_clock = 23;
        config.gpio_sensor_data = 24;
        config.gpio_sensor_di = 25;

        if self.config.thermocouple_type == 'MAX31855':
            log.info("init MAX31855")
            from max31855 import MAX31855, MAX31855Error
            self.thermocouple = MAX31855(config.gpio_sensor_cs,
                                     config.gpio_sensor_clock,
                                     config.gpio_sensor_data,
                                     config.temp_scale)

        if self.config.thermocouple_type == 'MAX31856':
            log.info("init MAX31856")
            from max31856 import MAX31856
            software_spi = { 'cs': config.gpio_sensor_cs,
                             'clk': config.gpio_sensor_clock,
                             'do': config.gpio_sensor_data,
                             'di': config.gpio_sensor_di }
            self.thermocouple = MAX31856(tc_type=MAX31856.MAX31856_S_TYPE,
                                         software_spi = software_spi,
                                         units = 'c', #config.temp_scale
                                         ac_freq_50hz = True, #config.ac_freq_50hz,
                                         )
        
        if self.config.thermocouple_type == 'DHT11':
            print('Sensor DHT11')
            self.DHT_SENSOR = Adafruit_DHT.DHT11
            self.DHT_PIN = 23

        if self.config.thermocouple_type == 'DS1820':
            os.system('modprobe w1-gpio')
            os.system('modprobe w1-therm')
            
            base_dir = '/sys/bus/w1/devices/'
            device_folder = glob.glob(base_dir + '28*')[0]
            self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c
        
    def run(self):
        '''use a moving average of config.temperature_average_samples across the time_step'''
        temps = []
        while True:
            # reset error counter if time is up
            if (time.time() - self.bad_stamp) > (self.time_step * 2):
                if self.bad_count + self.ok_count:
                    self.bad_percent = (self.bad_count / (self.bad_count + self.ok_count)) * 100
                else:
                    self.bad_percent = 0
                self.bad_count = 0
                self.ok_count = 0
                self.bad_stamp = time.time()
            if self.config.thermocouple_type == 'DHT11':
                humidity, temp = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
            elif self.config.thermocouple_type == 'DS1820':
                temp = self.read_temp()
                #print(temp)
            else:
                temp = self.thermocouple.get()
                self.noConnection = self.thermocouple.noConnection
                self.shortToGround = self.thermocouple.shortToGround
                self.shortToVCC = self.thermocouple.shortToVCC
                self.unknownError = self.thermocouple.unknownError
            
            print(f"temp in tempSensorReal {temp}")

            is_bad_value = self.noConnection | self.unknownError
            #if not config.ignore_tc_short_errors:
            #    is_bad_value |= self.shortToGround | self.shortToVCC

            if not is_bad_value:
                temps.append(temp)
                if len(temps) > self.config.temperature_average_samples:
                    del temps[0]
                self.ok_count += 1

            else:
                log.error("Problem reading temp N/C:%s GND:%s VCC:%s ???:%s" % (self.noConnection,self.shortToGround,self.shortToVCC,self.unknownError))
                self.bad_count += 1


            if len(temps):
                self.temperature = self.get_avg_temp(temps)
            time.sleep(self.sleeptime)

    def get_avg_temp(self, temps, chop=25):
        '''
        strip off chop percent from the beginning and end of the sorted temps
        then return the average of what is left
        '''
        chop = chop / 100
        temps = sorted(temps)
        total = len(temps)
        items = int(total*chop)
        temps = temps[items:total-items]
        return sum(temps) / len(temps)
