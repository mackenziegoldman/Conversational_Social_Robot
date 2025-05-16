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
        elif state == 2:
            # Person detected, tilt head up and down before landing on tilted up position

            pass
        elif state == 3:
            # Happy dance, tilt head left and right
            #servo does nothing in this state
            # dc motor, encoder, and controller code would go here
            pass
        elif state == 4:
            # Thinking pose, tilt head to the right and all the way up
            pass
        elif state == 5:
            # Speaking pose, tilt head up most the way but not all the way
            pass
        elif state == 6:
            # Idle/sleeping pose (kill signal goes here), tilt head down
            pass
        elif state == 7:
            # E-stop situation only, turn off motors
            #motor.disable()  # Turn off motors
            pass
        yield state






    # Motion profiles:

    # 2: Person detected, bob head up and down before landing on tilted up position
    # 3: Happy dance, tilt head left and right
    # 4: Thinking pose, tilt head to the right and all the way up
    # 5: Speaking pose, tilt head up most the way but not all the way
    # 6: Idle/sleeping pose, tilt head down (Kill goes here)
    # 7: E-stop situation only, turn off motors