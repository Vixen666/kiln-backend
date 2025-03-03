from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
import sys
import json
import RPi.GPIO as GPIO
import sys
sys.path.append('/home/pi/.local/lib/python3.9/site-packages')
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_dir + '/lib/')
from flask_cors import CORS
import random
import time
from threading import Thread, Event, Lock
import glob
import threading
from endpoints.oven_api import bp as oven_api_bp
from endpoints.template_api import bp as template_api_bp
from endpoints.template_curve_api import bp as template_curve_api_bp
from endpoints.image_api import bp as image_api_bp
from endpoints.burn_api import bp as burn_api_bp
from endpoints.burn_notes_api import bp as burn_notes_api_bp
from endpoints.burn_curve_api import bp as burn_curve_api_bp
from endpoints.template_util_api import bp as template_util_api_bp
from endpoints.generic_api import bp as generic_api_bp
from endpoints.test_api import bp as test_api_bp
from lib.board import Board

from services.function_services import FunctionServices
from services.generic_service import GenericService
from database import get_db_connection

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/pi/Development/upload/'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
function_services_instance = FunctionServices()
CORS(app)
app.register_blueprint(image_api_bp)
app.register_blueprint(oven_api_bp)
app.register_blueprint(template_api_bp)
app.register_blueprint(template_curve_api_bp)
app.register_blueprint(burn_api_bp, url_prefix='/api')
app.register_blueprint(test_api_bp, url_prefix='/api')
app.register_blueprint(burn_notes_api_bp)
app.register_blueprint(burn_curve_api_bp)
app.register_blueprint(template_util_api_bp)
app.register_blueprint(generic_api_bp, url_prefix='/api')
generic_service = GenericService(db_connection= get_db_connection())

thread = Thread()
thread_stop_event = Event()



class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __str__(self):
        attributes = ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

@socketio.on("connect", namespace="/ws/oven")
def handle_connect():
    #print("Client connected to WebSocket")
    emit("test_data", {"message": "Welcome! WebSocket is working."})

@socketio.on("disconnect", namespace="/ws/oven")
def handle_disconnect():
    print("Client disconnected from WebSocket")

# Event handler for starting the test
@socketio.on("start_test", namespace="/ws/oven")
def start_test(data):
    oven_id = data.get("oven_id", "unknown")
    #print("oven_id")
    oven_config = generic_service.execute_operation('OvenService', 'Get_By_Oven_Id', p_id=oven_id)
    wanted_oven = oven_config[0]
    wanted_oven = ConfigObject(wanted_oven)
    #print(wanted_oven)
    #print(f"starting {oven_id}")
    board = Board(wanted_oven)
    board.temp_sensor.run()
    for i in range(10):
        temp = board.temp_sensor.read_temp()
        #print(f"temp: {temp}")
        time.sleep(1)
        
    for i in range(10):
        # Start the test in a separate thread so it doesn't block the socket event loop
        #threading.Thread(target=test_oven, args=(oven_id,)).start()
        #time.sleep(1)
        temperature = random.randint(100, 300)  # Simulated temperature
        burner_status = random.choice(["ON", "OFF"])
        door_sensor = random.choice(["OPEN", "CLOSED"])

        # Emit test data back to the frontend (using socketio.emit)
        emit("test_data", {
            "temperature": temperature,
            "burner": burner_status,
            "door": door_sensor
        }, namespace='/ws/oven', broadcast=True)

if __name__ == '__main__':
    #app.run(debug=True, host="0.0.0.0")
    
    socketio.run(app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)