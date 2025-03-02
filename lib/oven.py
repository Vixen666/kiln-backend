import threading
import time
import random
import datetime
import logging
import json
import config
import os

from pid import PID
from profileCurve import Profile
from database import get_db_connection
log = logging.getLogger(__name__)
from services.generic_service import GenericService
generic_service = GenericService(db_connection= get_db_connection())
class DupFilter(object):
    def __init__(self):
        self.msgs = set()

    def filter(self, record):
        rv = record.msg not in self.msgs
        self.msgs.add(record.msg)
        return rv

class Duplogger():
    def __init__(self):
        self.log = logging.getLogger("%s.dupfree" % (__name__))
        dup_filter = DupFilter()
        self.log.addFilter(dup_filter)
    def logref(self):
        return self.log

duplog = Duplogger().logref()



class Oven(threading.Thread):
    '''parent oven class. this has all the common code
       for either a real or simulated oven'''
    def __init__(self, config, burn_id):
        print("Oven Class")
        threading.Thread.__init__(self)
        self.daemon = True
        self.temperature = 0
        self.time_step = config.sensor_time_wait
        self.config = config
        self.burn_id = burn_id
        self.reset()

    def reset(self):
        print("Oven reset")
        self.cost = 0
        self.state = "IDLE"
        self.previous_state = "IDLE"
        self.profile = None
        self.start_time = 0
        self.runtime = 0
        self.totaltime = 0
        self.target = 0
        self.heat = 0
        self.pid = PID(self.config, ki=self.config.pid_ki, kd=self.config.pid_kd, kp=self.config.pid_kp)

    def run_profile(self, profile, startat=0):
        print("Oven run_profile")
        self.reset()
        logmessages = []
        do_return = False
        if self.board.temp_sensor.noConnection:
            logmessages.append("Refusing to start profile - thermocouple not connected")
            do_return = True
        if self.board.temp_sensor.shortToGround:
            logmessages.append("Refusing to start profile - thermocouple short to ground")
            do_return = True
        if self.board.temp_sensor.shortToVCC:
            logmessages.append("Refusing to start profile - thermocouple short to VCC")
            do_return = True
        if self.board.temp_sensor.unknownError:
            logmessages.append("Refusing to start profile - thermocouple unknown error")    
            do_return = True

        if do_return:
            for message in logmessages:
                print(message)
                #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)
            return

        self.startat = startat
        self.runtime = self.startat
        self.start_time = datetime.datetime.now() - datetime.timedelta(seconds=self.startat)
        #print(f'self.start_time {self.start_time}')
        self.profile = profile
        self.totaltime = profile.get_duration()
        self.state = "RUNNING"
        #print("Starting at",  self.start_time)

    def abort_run(self):
        self.reset()
        self.save_automatic_restart_state()

    def kiln_must_catch_up(self):
        '''shift the whole schedule forward in time by one time_step
        to wait for the kiln to catch up'''
        if self.config.kiln_must_catch_up == True:
            temp = self.board.temp_sensor.temperature + \
                self.config.thermocouple_offset
            # kiln too cold, wait for it to heat up
            if self.target - temp > self.config.pid_control_window:
                #print("kiln must catch up, too cold, shifting schedule")
                message = "kiln must catch up, too cold, shifting schedule"
                #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)
                print(message)
                self.start_time = datetime.datetime.now() - datetime.timedelta(milliseconds = self.runtime * 1000)
            # kiln too hot, wait for it to cool down
            if temp - self.target > self.config.pid_control_window:
                message = "kiln must catch up, too hot, shifting schedule"
                #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)
                print(message)
                self.start_time = datetime.datetime.now() - datetime.timedelta(milliseconds = self.runtime * 1000)

    def update_runtime(self):
        runtime_delta = datetime.datetime.now() - self.start_time
        if runtime_delta.total_seconds() < 0:
            runtime_delta = datetime.timedelta(0)

        self.runtime = runtime_delta.total_seconds()

    def update_target_temp(self):
        self.target = self.profile.get_target_temperature(self.runtime)

    def reset_if_emergency(self):
        '''reset if the temperature is way TOO HOT, or other critical errors detected'''
        logmessages = []
        do_abort = False
        if (self.board.temp_sensor.temperature + self.config.thermocouple_offset >=
            self.config.emergency_shutoff_temp):
            logmessages.append("emergency!!! temperature too high")
            if self.config.ignore_temp_too_high == False:
                do_abort = True

        if self.board.temp_sensor.noConnection:
            logmessages.append("emergency!!! lost connection to thermocouple")
            if self.config.ignore_lost_connection_tc == False:
                do_abort = True
            
        if self.board.temp_sensor.unknownError:
            logmessages.append("emergency!!! unknown thermocouple error")
            if self.config.ignore_unknown_tc_error == False:
                do_abort = True
            
        if self.board.temp_sensor.bad_percent > 30:
            logmessages.append("emergency!!! too many errors in a short period")
            if self.config.ignore_too_many_tc_errors == False:
                do_abort = True
        
        
        if do_abort:
            self.abort_run()
            for message in logmessages:
                print(message)
                #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)


    def reset_if_schedule_ended(self):
        if self.runtime > self.totaltime:
            message = "schedule ended, shutting down"
            #print(message)
            #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)
            generic_service.execute_operation('BurnService', 'UpdateStatus', p_burn_id=self.burn_id, p_status='Finished')

            #log.info("total cost = %s%.2f" % (self.config.currency_type,self.cost))
            self.abort_run()

    def update_cost(self):
        return
        if self.heat:
            cost = (self.config.kwh_rate * self.config.kw_elements) * ((self.heat)/3600)
        else:
            cost = 0
        self.cost = self.cost + cost

    def get_state(self):
        temp = 0
        try:
            temp = self.board.temp_sensor.temperature + self.config.thermocouple_offset
        except AttributeError as error:
            # this happens at start-up with a simulated oven
            temp = 0
            pass

        state = {
            'cost': self.cost,
            'runtime': self.runtime,
            'temperature': temp,
            'target': self.target,
            'state': self.state,
            'heat': self.heat,
            'totaltime': self.totaltime,
            'kwh_rate': self.config.kwh_rate,
            'currency_type': self.config.currency_type,
            'profile': self.profile.name if self.profile else None,
            'pidstats': self.pid.pidstats,
        }
        return state

    def state_file_is_old(self):
        '''returns True is state files is older than 15 mins default
                   False if younger
                   True if state file cannot be opened or does not exist
        '''
        return False
        latest_temprow = generic_service.execute_operation('BurnTemperatureService', 'Get_Latest', p_burn_id=self.burn_id)
        if latest_temprow:
            latest_timestamp = latest_temprow["timestamp"]
            if latest_timestamp:
                now = time.time()
                minutes = (now - latest_timestamp)/60
                if(minutes <= self.config.automatic_restart_window):
                    return False
            return True
        return False


    def should_i_automatic_restart(self):
        # only automatic restart if the feature is enabled
        if self.config.automatic_restarts == 0:
            return False
        if self.state_file_is_old():
            message = "Latest temperature is old or missing, cannot restart"
            #print(message)
            #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)
            return False

        latest_burn_values = generic_service.execute_operation('BurnService', 'Get_By_Burn_Id', p_burn_id=self.burn_id)
        if latest_burn_values["status"] == "In Process123":
            message = "automatic restart not possible. state = %s" % (["status"])
            #print(message)
            #generic_service.execute_operation('BurnTemperatureService', 'Insert', p_burn_id=self.burn_id, p_message=message)
            return False

        return True

    def automatic_restart(self):
        
        startat = d["runtime"]/60
        filename = "%s.json" % (d["profile"])
        profile_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'storage','profiles',filename))

        log.info("automatically restarting profile = %s at minute = %d" % (profile_path,startat))
        with open(profile_path) as infile:
            profile_json = json.dumps(json.load(infile))
        profile = Profile(profile_json)
        self.run_profile(profile,startat=startat)
        self.cost = d["cost"]
        time.sleep(1)
        self.ovenwatcher.record(profile)

    def set_ovenwatcher(self,watcher):
        log.info("ovenwatcher set in oven class")
        self.ovenwatcher = watcher
    
    def is_open(self):
        hatchet = self.output.hatchet()
        if hatchet == -1:
            return False
        
        hatchet_mode = self.config.hatchet_mode
        
        if hatchet_mode == 'HIGH_OPEN':
            return hatchet == 1
        
        return hatchet == 0
    
    def check_open(self):
        if self.is_open():
            self.state = "OPEN"
            return
        self.state = self.previous_state
        
        
    def run(self):
        while True:
            self.check_open()
            if self.state == "IDLE":
                if self.should_i_automatic_restart() == True:
                    #self.automatic_restart()
                    None
                self.state = "RUNNING"
                time.sleep(1)
                self.previous_state = "IDLE"
            if self.state == "RUNNING":
                self.update_cost()
                self.kiln_must_catch_up()
                self.update_runtime()
                self.update_target_temp()
                self.heat_then_cool()
                self.reset_if_emergency()
                self.reset_if_schedule_ended()
                self.previous_state = "RUNNING"
            if self.state == "OPEN":
                continue



