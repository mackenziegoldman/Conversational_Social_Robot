# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

import pyb
from pyb import Pin, Timer
import cotask
import task_share
from servo import Servo
from motor import Motor
from encoder import Encoder
from controller import PIDController

def motion_profiles(shares):
    """Motion profiles task for controlling the robot's movement."""
    motion_profile_state, motion_profile, kill_message, servo = shares
    state = motion_profile_state.get()

    while True:
        state = motion_profile_state.get()
        if state == 1:
            # WAIT state
            if kill_message.get() == 1:  # The KILL message has been received
                motion_profile_state.put(6)
            elif motion_profile.get() == 1:
                motion_profile_state.put(1)
            elif motion_profile.get() == 2:
                motion_profile_state.put(2)
            elif motion_profile.get() == 3:
                motion_profile_state.put(3)
            elif motion_profile.get() == 4:
                motion_profile_state.put(4)
            elif motion_profile.get() == 5:
                motion_profile_state.put(5)
            elif motion_profile.get() == 6:
                motion_profile_state.put(6)
            elif motion_profile.get() == 7:
                motion_profile_state.put(7)
        elif state == 2:
            # Person detected, tilt head up and down before landing on tilted up position
            if not hasattr(motion_profiles, "move_task") or motion_profiles.move_task is None:
                def sweep_generator():
                    # Sweep up to 1090 us
                    current_us = 740
                    while current_us < 1090:
                        current_us += 5
                        if current_us > 1090:
                            current_us = 1090
                        servo.write_us(current_us)
                        pyb.delay(10)
                        yield
                    # Sweep down to 740 us
                    while current_us > 740:
                        current_us -= 5
                        if current_us < 740:
                            current_us = 740
                        servo.write_us(current_us)
                        pyb.delay(10)
                        yield
                    # Sweep back up to 1090 us
                    while current_us < 1090:
                        current_us += 5
                        if current_us > 1090:
                            current_us = 1090
                        servo.write_us(current_us)
                        pyb.delay(10)
                        yield
                motion_profiles.move_task = sweep_generator()
                motion_profiles.move_task_active = True

            if motion_profiles.move_task_active:
                try:
                    next(motion_profiles.move_task)  # Advance the servo movement
                    pyb.delay(1)  # Delay between steps (short, non-blocking)
                except StopIteration:
                    print("Servo movement complete")
                    motion_profiles.move_task = None
                    motion_profiles.move_task_active = False
                    motion_profile_state.put(1)  
            yield state
        elif state == 3:
            # Happy dance, tilt head left and right
            #servo does nothing in this state
            # dc motor, encoder, and controller code would go here
            motion_profile_state.put(1)  
        elif state == 4:
            # Thinking pose, tilt head to the right and all the way up
            motion_profile_state.put(1)  
        elif state == 5:
            # Speaking pose, tilt head up most the way but not all the way
            if not hasattr(motion_profiles, "move_task") or motion_profiles.move_task is None:
                # Only create the move task once per state entry
                motion_profiles.move_task = servo.move_to(30, speed=2)
                motion_profiles.move_task_active = True

            if motion_profiles.move_task_active:
                try:
                    next(motion_profiles.move_task)  # Advance the servo movement
                    pyb.delay(1)  # Delay between steps (short, non-blocking)
                except StopIteration:
                    print("Servo movement complete")
                    motion_profiles.move_task = None
                    motion_profiles.move_task_active = False
                    motion_profile_state.put(1)  
            yield state

        elif state == 6:
            # Idle/sleeping pose (kill signal goes here), tilt head down
            if not hasattr(motion_profiles, "move_task") or motion_profiles.move_task is None:
                # Only create the move task once per state entry
                motion_profiles.move_task = servo.move_to(0, speed=2)
                motion_profiles.move_task_active = True
            if motion_profiles.move_task_active:
                try:
                    next(motion_profiles.move_task)  # Advance the servo movement
                    pyb.delay(1)  # Delay between steps (short, non-blocking)
                except StopIteration:
                    print("Servo movement complete")
                    motion_profiles.move_task = None
                    motion_profiles.move_task_active = False
                    motion_profile_state.put(1)  
            yield state
        elif state == 7:
            # E-stop situation only, turn off motors
            #motor.disable()  # Turn off motors
            motion_profile_state.put(1)  
        yield state

    # Motion profiles:

    # 2: Person detected, bob head up and down before landing on tilted up position
    # 3: Happy dance, tilt head left and right
    # 4: Thinking pose, tilt head to the right and all the way up
    # 5: Speaking pose, tilt head up most the way but not all the way
    # 6: Idle/sleeping pose, tilt head down ("KILL" goes here)
    # 7: E-stop situation only, turn off motors

# E-stop use case:
    # Motor errors from fault pin on motor driver
#     DRV8838 Fault Detection:
#       Use the FAULT pin to detect overcurrent (1.8A), thermal shutdown, or undervoltage conditions.
#       Monitor the FAULT pin 
        # class Motor:
        #     def __init__(self, pin_enable, pin_fault, min_position, max_position):
        #         self.enable_pin = pyb.Pin(pin_enable, pyb.Pin.OUT)
        #         self.fault_pin = pyb.Pin(pin_fault, pyb.Pin.IN, pyb.Pin.PULL_UP)  # Input with pull-up
        #         self.min_position = min_position
        #         self.max_position = max_position
        #         self.current_position = 0  # Placeholder for motor position (e.g., from encoder)

        #     def has_fault(self):
        #         """Check if the motor driver reports a fault."""
        #         return self.fault_pin.value() == 0  # FAULT pin is low when a fault occurs

        #     def is_out_of_bounds(self):
        #         """Check if the motor's position is out of bounds."""
        #         return self.current_position < self.min_position or self.current_position > self.max_position
        # if state == 1:
        #     # Check for motor errors
        #     motor_fault = motor.has_fault()  # Check for fault signals
        #     motor_out_of_bounds = motor.is_out_of_bounds()  # Check for out-of-bounds movement

        #     # If any error is detected, transition to state 7
        #     if motor_fault or motor_out_of_bounds:
        #         print("Motor error detected! Transitioning to Kill Pose (state 7).")
        #         motion_profile_state.put(7)  # Transition to Kill Pose

        # elif state == 7:
        #     # Kill pose (E-stop situation only)
        #     print("State 7: Emergency stop activated. Shutting down motors.")

        #     # Disable motors and servo
        #     motor.disable()
        #     pyb.Pin('POWER_PIN', pyb.Pin.OUT).low()  # Replace 'POWER_PIN' with the actual pin controlling power

        #     print("Motors and servo disabled.")
        #     yield state

