# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

import pyb
from IR_sensor import MOT2002_IR
import cotask
import task_share

def sensor(shares):
    """Sensor task for reading the IR sensor."""
    sensor_triggered, ir_sensor_state, IR_sens, kill_message, comm_message = shares
    state = ir_sensor_state.get()
    person_present = False 

    while True:
        state = ir_sensor_state.get()
        if state == 1: # WAIT
            #triggered = sensor_triggered.get()
            sensor_reading = IR_sens.logical_value()
            #print(f"Sensor reading: {sensor_reading}")
            #raw_value = IR_sens.read_raw()
            #print(f"Raw value: {raw_value}")
            #print(f"Person Present = {person_present}")

            if kill_message.get()==1: #The KILL message has been received
                ir_sensor_state.put(3)

            elif sensor_reading == 0:
                if person_present:  # If a person was previously detected
                     # Add a timeout before sending the KILL message
                    if no_motion_timer is None:  # Start the timer
                        no_motion_timer = pyb.millis()
                    elif pyb.elapsed_millis(no_motion_timer) > 5000:  # 5-second timeout
                        comm_message.put(2)  # Send KILL message
                        sensor_triggered.put(0)  # Reset the sensor trigger flag
                        person_present = False
                        no_motion_timer = None  # Clear the timer
                    else:
                        ir_sensor_state.put(1)

            elif sensor_reading == 1:  # Motion detected
                if not person_present:  # Motion detected for the first time
                    print("Motion detected!")
                    person_present = True
                    ir_sensor_state.put(2)  # Transition to State 2 to send START message
                else:
                    ir_sensor_state.put(1)  # Stay in WAIT state
                no_motion_timer = None  # Clear the timer if motion resumes
            yield state

        elif state == 2: # SENSOR TRIGGERED FIRST TIME
            # If the sensor detects motion, activate the flag
            print("Sensor triggered!")
            if sensor_triggered.get() == 1:
                ir_sensor_state.put(1)
            else:
                print("Comm message put in queue")
                sensor_triggered.put(1)
                comm_message.put(1)  # Send START message
                print(f"[Comms Task] Queue size: {comm_message.num_in()}")
                ir_sensor_state.put(1)   
            yield state
        
        elif state == 3: #"KILL" message received
            sensor_triggered.put(0)
            kill_message.put(0)
            ir_sensor_state.put(1)
            yield state
