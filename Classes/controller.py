from pyb import Pin, Timer
import time

class PIDController:
    '''A PID controller class for motor control'''
    def __init__(self, kp, ki, kd, setpoint=0):
        '''Initializes the PID controller with given gains and setpoint'''
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0
        self.previous_error = 0
        self.previous_time = time.ticks_ms()

    def compute(self, measurement):
        '''Computes the control effort based on the measurement'''
        current_time = time.ticks_ms()
        dt = time.ticks_diff(current_time, self.previous_time) / 1000.0  # Convert ms to seconds
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt if dt > 0 else 0

        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        self.previous_error = error
        self.previous_time = current_time

        return output

    def set_setpoint(self, setpoint):
        '''Sets a new setpoint for the PID controller'''
        self.setpoint = setpoint
        self.integral = 0
        self.previous_error = 0
        self.previous_time = time.ticks_ms()
