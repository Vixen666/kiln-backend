import threading

class TempSensor(threading.Thread):
    def __init__(self, sensor_time_wait):
        threading.Thread.__init__(self)
        self.daemon = True
        self.temperature = 0
        self.bad_percent = 0
        self.time_step = sensor_time_wait
        self.noConnection = self.shortToGround = self.shortToVCC = self.unknownError = False
