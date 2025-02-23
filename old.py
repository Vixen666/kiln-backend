@app.route('/start_temperature_regulation', methods=['GET'])
def start_temperature_regulation():
    burn_id = request.args.get('burn_id')
    print("start_temperature_regulation")
    if burn_id is None:
        return jsonify({'error': 'No burn_id provided'}), 400

    sequences = get_curve_data(burn_id)
    if sequences:
        print("Got sequences")
        regulation_thread = threading.Thread(target=regulate_temperature, args=(sequences,burn_id))
        regulation_thread.start()
        return jsonify({'message': 'Temperature regulation started for burn_id {}'.format(burn_id)}), 200
    else:
        return jsonify({'error': 'Failed to fetch data or no data available for burn_id {}'.format(burn_id)}), 500

def get_temp_test(current_temp, heating):

    if heating:
        return current_temp + 5
    else:
        return current_temp - 2


def regulate_temperature(sequences, burn_id):
    current_temp = 10
    for seq in sequences:
        heating = False  # Flag to indicate if we are currently heating

        sequence, target_time, startTemp, endTemp = seq['sequence'], seq['time'], seq['startTemp'], seq['endTemp']
        start_time = time.time() 
        target_time = target_time
        while True: 
            current_time = time.time()
            elapsed_time = current_time - start_time
            time_percentage = (elapsed_time / target_time) if target_time else 0
            current_target_temp = startTemp + (endTemp - startTemp) * time_percentage 
            current_temp = get_temp_test(current_temp, heating)

            print("Temp={0:0.1f}*C  Goal={1:0.1f} TimeElapsed={2:0.1f}".format(current_temp, current_target_temp, elapsed_time))
            # Turn on the burner if below target and not currently heating
            if current_temp <= current_target_temp and not heating:
                burn(True)
                heating = True

            # Turn off the burner if above target or if time for the sequence is up
            if current_temp >= current_target_temp and heating:
                burn(False)
                heating = False
            
            # When target time == 0 and we have reached the correct temperature move to next sequence 
            if target_time == 0 and current_temp >= current_target_temp:
                burn(False)
                heating = False
                break  # Move to the next sequence

            # If we have reached target time, and target time is not 0, move to next sequence
            if time.time() - start_time >= target_time and target_time != 0:
                burn(False)
                heating = False
                break  # Move to the next sequence

            # Save the reading to the database
            save_temperature_reading(current_temp, burn_id, heating)
            # Sleep for a short duration before checking the temperature again
            
            time.sleep(1)

        # Small delay before starting the next sequence
        time.sleep(2)
    GPIO.cleanup()


def save_temperature_reading(temperature, burn_id, heating):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        cursor.callproc('Burn_Temperature_Api_Insert', [temperature, burn_id, heating])
        conn.commit()
    except Exception as e:
        print("Error saving temperature reading:", e)
    finally:
        cursor.close()
        conn.close()

def burn(value_):
    GPIO.output(GPIO_PIN, GPIO.HIGH if value_ else GPIO.LOW)

def get_temp():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is None or temperature is None:
        print("Failed to retrieve data from humidity sensor")
    return temperature








GPIO_PIN = 24
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
GPIO.setup(GPIO_PIN, GPIO.OUT)
GPIO.output(GPIO_PIN, GPIO.LOW )

def burn(value_):
    GPIO.output(GPIO_PIN, GPIO.HIGH if value_ else GPIO.LOW)


DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 23
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

@app.route('/start_burn', methods=['GET'])
def start_burn():
    while True:
        #humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        #print(f"Temp={temperature:.1f}*C Humidity={humidity:.1f}%")
        temp_c = read_temp()
        print(temp_c)
        if temp_c is not None:
            if temp_c >= 65:
                burn(0)
            else:
                print("burning!")
                burn(1) 
        time.sleep(2)
        burn(0)
        #if humidity is None or temperature is None:
            #print("Failed to retrieve data from humidity sensor")
        time.sleep(1)
    return {'temp': '%.2f' % temperature}, 200

sequence = 0
@app.route('/get_temp', methods=['GET'])
def get_temp():
    temp_c = read_temp()
    global sequence
    sequence += 1
    return {'sequence': sequence,'temperature': '%.2f' % temp_c}, 200


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c



# Set up GPIO pin
#GPIO_PIN = 24
#GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme
#GPIO.setup(GPIO_PIN, GPIO.OUT)
#GPIO.output(GPIO_PIN, GPIO.LOW)
#state = 0
#
#pwm = GPIO.PWM(GPIO_PIN, 10000)
#current_duty_cycle = 0
#pwm.start(current_duty_cycle)
#    
#@app.route('/increase', methods=['POST'])
#def increase():
#    global current_duty_cycle
#    current_duty_cycle = current_duty_cycle + 2
#    pwm.ChangeDutyCycle(current_duty_cycle)  # Set duty cycle
#    return jsonify(success=True, state=current_duty_cycle)