from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
from services.generic_service import GenericService
import time
from lib.output import Output
import Adafruit_DHT
import glob
import os
generic_service = GenericService(db_connection= get_db_connection())

bp = Blueprint('test_api', __name__)

class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __str__(self):
        attributes = ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

def get_temp(wanted_oven):
    temp = 0
    
    if wanted_oven.thermocouple_type == 'MAX31855':
        from max31855 import MAX31855, MAX31855Error
        thermocouple = MAX31855(wanted_oven.gpio_sensor_cs,
                                wanted_oven.gpio_sensor_clock,
                                wanted_oven.gpio_sensor_data,
                                wanted_oven.temp_scale)

    if wanted_oven.thermocouple_type == 'MAX31856':
        from max31856 import MAX31856
        software_spi = { 'cs': wanted_oven.gpio_sensor_cs,
                            'clk': wanted_oven.gpio_sensor_clock,
                            'do': wanted_oven.gpio_sensor_data,
                            'di': wanted_oven.gpio_sensor_di }
        thermocouple = MAX31856(tc_type=MAX31856.MAX31856_S_TYPE,
                                        software_spi = software_spi,
                                        units = 'c', #config.temp_scale
                                        ac_freq_50hz = True, #config.ac_freq_50hz,
                                        )

    if wanted_oven.thermocouple_type == 'DS1820':
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
     
    
    if wanted_oven.thermocouple_type == 'DHT11':
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, wanted_oven.gpio_sensor_cs)
    elif wanted_oven.thermocouple_type == 'DS1820':
        temp = read_temp(device_file)
    else:
        temp = thermocouple.get()
    
    #print((temp)
    return {"temp": temp}, 200

@bp.route('/test_temp', methods=['POST'])
def start_test():
    data = request.get_json()
    oven_id = data.get("oven_id", "unknown")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config
    wanted_oven = ConfigObject(wanted_oven)
    
    return get_temp(wanted_oven)
    

@bp.route('/test_hatchet', methods=['POST'])
def test_hatchet():
    data = request.get_json()
    oven_id = data.get("oven_id", "unknown")
    #print(("oven_id")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config
    wanted_oven = ConfigObject(wanted_oven)
    output = Output(wanted_oven)
    hatchet = output.hatchet()
    if hatchet == -1:
        return {"hatchet":"No hatchet-pin defined."}
    
    hatchet_mode = wanted_oven.hatchet_mode
        
        
        
    if hatchet_mode == 'HIGH_OPEN':
        return {"hatchet":"OPEN"} if hatchet == 1 else {"hatchet":"CLOSED"}
    
    return {"hatchet":"OPEN"} if hatchet == 0 else {"hatchet":"CLOSED"}

@bp.route('/test_outputs', methods=['POST'])
def test_outputs():  
    data = request.get_json()
    oven_id = data.get("oven_id", "unknown")
    #print(("oven_id")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config
    wanted_oven = ConfigObject(wanted_oven)
    output = Output(wanted_oven)
    for i in range(5):
        output.heat(1)
        output.cool(1)

    output.failsafe()    
    for i in range(5):
        output.heat(1)
        output.cool(1)
    return jsonify({"status": 1}), 200
        
def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c