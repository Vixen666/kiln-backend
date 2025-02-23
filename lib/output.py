import time
import logging

log = logging.getLogger(__name__)

class Output(object):
    def __init__(self, wanted_oven):
        self.config = wanted_oven        
        self.active = False
        self.load_libs()

    def load_libs(self):
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            if self.config.gpio_heat:
                GPIO.setup(self.config.gpio_heat, GPIO.OUT)
            if self.config.gpio_cool and self.config.gpio_cool != 0:
                GPIO.setup(self.config.gpio_cool, GPIO.OUT)

            if self.config.gpio_failsafe:
                GPIO.setup(self.config.gpio_failsafe, GPIO.OUT)
                GPIO.output(self.config.gpio_failsafe, GPIO.HIGH)

            if self.config.gpio_hatchet:
                print(f"self.config.gpio_hatchet: {self.config.gpio_hatchet}")
                GPIO.setup(self.config.gpio_hatchet, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Pull-down to GND
            self.active = True
            self.GPIO = GPIO  # Assign after successful initialization

        except Exception as e: 
            print(e)
            log.warning("Could not initialize GPIOs, oven operation will only be simulated!")
            self.active = False

    def heat(self, sleepfor):
        print(f"self.config.gpio_heat {self.config.gpio_heat}")
        self.GPIO.output(self.config.gpio_heat, self.GPIO.HIGH)
        if self.config.gpio_cool:
            self.GPIO.output(self.config.gpio_cool, self.GPIO.LOW)
        time.sleep(sleepfor)

    def cool(self, sleepfor):
        '''No active cooling, so sleep'''
        self.GPIO.output(self.config.gpio_heat, self.GPIO.LOW)
        time.sleep(sleepfor)

    def active_cool(self, sleepfor):
        '''Active cooling'''
        self.GPIO.output(self.config.gpio_heat, self.GPIO.LOW)
        if self.config.gpio_cool:
            self.GPIO.output(self.config.gpio_cool, self.GPIO.HIGH)
        time.sleep(sleepfor)
        
    def failsafe(self):
        print(f"self.config.gpio_failsafe {self.config.gpio_failsafe}")
        self.GPIO.output(self.config.gpio_failsafe, self.GPIO.LOW)
        
    def hatchet(self):
        print(f"self.GPIO.input(self.config.gpio_hatchet: {self.GPIO.input(self.config.gpio_hatchet)}")
        if not self.config.gpio_hatchet:
            return -1
        return self.GPIO.input(self.config.gpio_hatchet)