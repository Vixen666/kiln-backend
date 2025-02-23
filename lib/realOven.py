import threading
import time
import random
import datetime
import logging
import json
import config
import os
from database import get_db_connection
from oven import Oven
from output import Output
from board import Board
from services.generic_service import GenericService
generic_service = GenericService(db_connection= get_db_connection())
log = logging.getLogger(__name__)

class ConfigObject:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            setattr(self, key, value)
    def __str__(self):
        attributes = ", ".join([f"{key}: {value}" for key, value in self.__dict__.items()])
        return f"{self.__class__.__name__}({attributes})"

class RealOven(Oven):

    def __init__(self, wanted_oven, burn_id):
        self.config = wanted_oven
        print('Real Oven Config', self.config)
        self.board = Board(wanted_oven)
        self.output = Output(wanted_oven)
        self.burn_id = burn_id
        self.reset()

        # call parent init
        Oven.__init__(self, self.config, burn_id)

        # start thread
        self.start()

    def reset(self):
        super().reset()
        self.output.cool(0)

    def heat_then_cool(self):
        pid = self.pid.compute(self.target,
                               self.board.temp_sensor.temperature +
                               self.config.thermocouple_offset)
        heat_on = float(self.time_step * pid)
        heat_off = float(self.time_step * (1 - pid))

        # self.heat is for the front end to display if the heat is on
        self.heat = 0.0
        if heat_on > 0:
            self.heat = 1.0

        if heat_on:
            self.output.heat(heat_on)
        if heat_off:
            self.output.cool(heat_off)
        #if heat_off and self.pid.pidstats['err'] < -self.config.cool_window:
        #    self.output.active_cool(heat_off)
        

        time_left = self.totaltime - self.runtime
        generic_service.execute_operation('BurnTemperatureService', 'Insert', 
                                            p_burn_id = self.burn_id,
                                            p_ispoint = self.pid.pidstats['ispoint'],
                                            p_setpoint = self.pid.pidstats['setpoint'],
                                            p_err = self.pid.pidstats['err'],
                                            p_pid = self.pid.pidstats['pid'],
                                            p_p = self.pid.pidstats['p'],
                                            p_i = self.pid.pidstats['i'],
                                            p_d = self.pid.pidstats['d'],
                                            p_heat_on = heat_on,
                                            p_heat_off = heat_off,
                                            p_runtime = self.runtime)
        
        
        try:
            log.info("temp=%.2f, target=%.2f, error=%.2f, pid=%.2f, p=%.2f, i=%.2f, d=%.2f, heat_on=%.2f, heat_off=%.2f, run_time=%d, total_time=%d, time_left=%d" %
                (self.pid.pidstats['ispoint'],
                self.pid.pidstats['setpoint'],
                self.pid.pidstats['err'],
                self.pid.pidstats['pid'],
                self.pid.pidstats['p'],
                self.pid.pidstats['i'],
                self.pid.pidstats['d'],
                heat_on,
                heat_off,
                self.runtime,
                self.totaltime,
                time_left))
        except KeyError:
            pass
