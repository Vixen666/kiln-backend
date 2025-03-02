from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
import functools
from services.generic_service import GenericService
from simulatedOven import SimulatedOven
from realOven import RealOven
from profileCurve import Profile
from ovenWatcher import OvenWatcher
from threading import Thread, Event, Lock
import time
import json
from lib.board import Board
from lib.output import Output
import Adafruit_DHT
import glob
import os
generic_service = GenericService(db_connection= get_db_connection())

bp = Blueprint('burn_api', __name__)

class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __str__(self):
        attributes = ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

def create_burn_and_copy_curve(oven_id, template_id, description):
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Call the procedure to create a burn and get the new burn_id
            cursor.callproc('Burn_Api_Create_Burn', [oven_id, template_id, description])
            
            # Fetch the result of the new burn_id
            new_burn_id = None
            for result in cursor.stored_results():
                new_burn_id = result.fetchone()[0]
                
            # Call the procedure to copy the template curve to the burn curve
            cursor.callproc('Burn_Curve_Api_Copy_Template_Curve', [new_burn_id, template_id])
            
            connection.commit()
            return new_burn_id
    except Error as e:
        #print(("Error while connecting to MySQL", e)
        if connection.is_connected():
            connection.rollback()
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def copy_burn_parameters(burn_id):
    try:
        connection = get_db_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Call the procedure to create a burn and get the new burn_id
            cursor.callproc('Burn_Parameters_Api_Insert', [burn_id])

            connection.commit()
    except Error as e:
        #print(("Error while connecting to MySQL", e)
        if connection.is_connected():
            connection.rollback()
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@bp.route('/Burn_Api_Create_Burn', methods=['POST'])
def Burn_Api_Create_Burn():
    data = request.get_json()
    oven_id = data.get('oven_id')
    template_id = data.get('template_id')
    description = data.get('description', '')  # Default to empty string if not provided
    
    new_burn_id = create_burn_and_copy_curve(oven_id, template_id, description)
    #copy_burn_parameters(new_burn_id)
    if new_burn_id is not None:
        return jsonify({'message': 'Burn created successfully', 'burn_id': new_burn_id}), 200
    else:
        return jsonify({'error': 'Failed to create burn'}), 500
    

@bp.route('/start_simulation', methods=['POST'])
def start_simulation():
    data = request.get_json()
    profile_id = data.get('profile_id')
    oven_id = data.get('oven_id')
    startat_ = data.get('startat_')
    #wanted_oven {PID, PINS, time_step}  = Oven_Api_Get_Setup(oven_id)
    #print(("Staring Simulation")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config[0]
    #print((json.dumps(wanted_oven, indent=4))
    oven = SimulatedOven(wanted_oven)
    ovenWatcher = OvenWatcher(oven)
    wanted = profile_id
    startat = 0;      
    if startat_:
        startat = startat_

    # get the wanted profile/kiln schedule
    profile = wanted
    if profile is None:
        return { "success" : False, "error" : "profile %s not found" % wanted }

    # FIXME juggling of json should happen in the Profile class
    profile_json = generic_service.execute_operation('BurnCurveService', 'Get_Curve_By_Id', p_burn_id=profile_id)
    transformed_data = {
    "data": [[entry["time"], entry["temperature"]] for entry in profile_json[0]]
    }
    profile = Profile(transformed_data)
    oven.run_profile(profile,startat=startat)
    ovenWatcher.record(profile)
    return "Started!"

ongoing_burns = {}
burn_lock = Lock()

@bp.route('/start_real', methods=['POST'])
def start_real():
    data = request.get_json()
    burn_id = data.get('burn_id')
    burn_json = generic_service.execute_operation('BurnService', 'Get_By_Burn_Id', p_burn_id=burn_id)
    oven_id = burn_json['oven_id']
    startat_ = 0
    #print(("Starting Real")
    wanted_oven = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = ConfigObject(wanted_oven)
    oven = RealOven(wanted_oven, burn_id)
    ovenWatcher = OvenWatcher(oven)
    startat = 0
    if startat_:
        startat = startat_
    
    profile_json = generic_service.execute_operation('BurnCurveService', 'Get_Curve_By_Id', p_burn_id=burn_id)
    #print(("kommer man hit?!?!?")
    #print((profile_json)
    #print(("Och sen hit?!?!?")
    cumulative_time = 0

    transformed_data = {"data": []}
    for entry in profile_json:
        #print((entry['time'], entry['temperature'])
        cumulative_time += entry['time']
        
        transformed_data['data'].append([cumulative_time * 60, entry['temperature']])

    profile = Profile(transformed_data)
    oven.run_profile(profile, startat=startat)
    ovenWatcher.record(profile)
    #generic_service.execute_operation('BurnService', 'UpdateStatus', p_burn_id=burn_id, p_status='In Process')
    with burn_lock:
        ongoing_burns[burn_id] = oven

    return "Started!"

@bp.route('/stop_real', methods=['POST'])
def stop_real():
    data = request.get_json()
    burn_id = data.get('burn_id')
    
    with burn_lock:
        if burn_id in ongoing_burns:
            oven = ongoing_burns.pop(burn_id)
            oven.reset()
            generic_service.execute_operation('BurnService', 'UpdateStatus', p_burn_id=burn_id, p_status='Cancelled')
            return f"Burn {burn_id} stopped!"
        else:
            return f"Burn {burn_id} not found!", 404
        
@bp.route('/test_temp', methods=['POST'])
def start_test():
    data = request.get_json()
    oven_id = data.get("oven_id", "unknown")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config[0]
    wanted_oven = ConfigObject(wanted_oven)
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
        #print((f"reading DHT11??? {wanted_oven.gpio_sensor_cs}")
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, wanted_oven.gpio_sensor_cs)
    elif wanted_oven.thermocouple_type == 'DS1820':
        temp = read_temp(device_file)
    else:
        temp = thermocouple.get()
    
    #print((temp)
    return {"temp": temp}, 200

@bp.route('/test_hatchet', methods=['POST'])
def test_hatchet():
    data = request.get_json()
    oven_id = data.get("oven_id", "unknown")
    #print(("oven_id")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config[0]
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
    wanted_oven = oven_config[0]
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