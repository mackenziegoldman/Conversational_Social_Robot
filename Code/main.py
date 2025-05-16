# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

import gc
import pyb
from pyb import USB_VCP, Pin, UART
import cotask
import task_share
#from motor import Motor
#from encoder import Encoder
from IR_sensor import MOT2002_IR
from servo import Servo
#from controller import PIDController
import time
from comms_task import comms
from sensor_task import sensor as IR_sensor
from motion_task import motion_profiles

class SystemInitializer:
    def __init__(self, IR_sens, comms_state, ir_sensor_state, sensor_triggered, kill_message):
        """Initialization task which is run once at startup to set 
        up necessary components."""
        print("[Init] Initializing system...")
        #self.encoder = encoder
        #self.motor = motor
        #self.servo = servo
        self.IR_sens = IR_sens
        self.sensor_triggered = sensor_triggered
        self.kill_message = kill_message
        self.comms_state = comms_state
        self.ir_sensor_state = ir_sensor_state
        #self.motor_state = motor_state
        #self.servo_state = servo_state
        self.bluetooth = UART(1, 115200, timeout=1000)  # Bluetooth UART
        self.bt_state_pin = Pin('B14', Pin.IN)  # Replace 'X1' with the actual pin connected to the STATE pin

        # Set initial states
        self.comms_state.put(1)  # Set initial state to 1 (WAIT)
        self.ir_sensor_state.put(1)  # Set initial state to 1 (WAIT)
        #self.motor_state.put(1)  # Set initial state to 1 (WAIT)
        #self.servo_state.put(1)  # Set initial state to 1 (WAIT)
        #

        # Zero the encoder
        #self.zero_encoder()

        # Initialize motor
        #self.initialize_motor()

        # Initialize servo
        #self.initialize_sero()

        # Initialize IR sensor
        self.initialize_IR_sensor()
        #time.sleep_ms(3000)

        # Wait for Bluetooth connection
        self.wait_for_bluetooth_connection()

    def wait_for_bluetooth_connection(self):
        """Wait until a Bluetooth connection is established."""
        print("[Init] Checking Bluetooth connection...")
        while self.bt_state_pin.value() != 1:  # Repeat until the connection is established
            print("Waiting for Bluetooth connection...")
            pyb.delay(500)  # Wait for 500ms before checking again

        print("[Init] Bluetooth connected!")

    def zero_encoder(self):
        """Zero the encoder."""
        self.encoder.zero()
        print("[Init] Encoder zeroed.")

    def initialize_motor(self):
        """Initialize the motor."""
        self.motor.disable()
        print("[Init] Motor initialized and disabled.")
    
    def initialize_IR_sensor(self):
        """Initialize the IR sensor."""
        self.IR_sens.enable()
        self.sensor_triggered.put(0)  # Reset the sensor trigger flag
        self.kill_message.put(0)  # Reset the KILL message flag
        print("[Init] IR sensor initialized and enabled.")

    def initialize_servo(self):
        """Initialize the servo."""
        #self.servo.enable()
        print("[Init] Servo initialized and disabled.")


if __name__ == "__main__":
    # Create instances of the encoders, motors, and servos
    #encoder = Encoder(3, 'A6', 'A7')
    #motor = Motor(4, 1,'B6', 'C8', 'C7')
    #servo = Servo(2, 'A15')
    #controller = PIDController(10, 0, 0.0002)
    IR_sens = MOT2002_IR('B1')



    # Create a share and a queue to test function and diagnostic printouts
    effort_share = task_share.Share('h', thread_protect=False, 
                                      name="effort_share")
    pos_queue = task_share.Queue('f', 100, thread_protect=False, 
                                        overwrite=False, name="pos_queue")
    sensor_triggered = task_share.Share('b', thread_protect=False,
                                        name="sensor_triggered")  # Shared flag
    kill_message = task_share.Share('h', thread_protect=False,
                                        name="kill_message")  # KILL message flag
    comm_message = task_share.Queue('h', 20, thread_protect=False, 
                                        overwrite=False, name="comm_message")
    motion_profile = task_share.Share('h', thread_protect=False,
                                        name="motion_profile") 

    comms_state = task_share.Share('h', thread_protect=False,
                                        name="comms_state") 
    ir_sensor_state = task_share.Share('h', thread_protect=False,
                                        name="ir_sensor_state") 
    motion_profile_state = task_share.Share('h', thread_protect=False,
                                        name="motion_profile_state")                                

# Initialize the system
    initializer = SystemInitializer(IR_sens, comms_state, ir_sensor_state, sensor_triggered, kill_message)

# Create the tasks.
    # motor_task = cotask.Task(motor, name=" motor", priority=3, 
    #                     period=10, profile=True, trace=False, 
    #                     shares=(R_effort_share,R_pos_queue, R_vel_queue,
    #                     data_collection_complete,))

    comms_task = cotask.Task(comms, name="comms", priority=2, period=750,
                            profile=True, trace=False, 
                            shares=(comms_state, comm_message, kill_message, initializer.bluetooth)) 

    IR_sensor_task = cotask.Task(IR_sensor, name="IR_sensor", 
                         priority=2, period=10, profile=True, trace=False,
                         shares = (sensor_triggered, ir_sensor_state, 
                                   IR_sens, kill_message, comm_message))
    # motion_profile_task = cotask.Task(motion_profiles, name="motion_profiles",
    #                      priority=2, period=10, profile=True, trace=False,
    #                      shares = (motion_profile_state, motion_profile, kill_message, servo))
    
    # mot_controller_task = cotask.Task(mot_controller, name="mot_controller", 
    #                     priority=2, period=10, profile=True, trace=False,
    #                     shares = (line_position_queue,R_effort_share,
    #                     L_effort_share))

    cotask.task_list.append(comms_task)
    #cotask.task_list.append(motor_task)
    cotask.task_list.append(IR_sensor_task)
    # cotask.task_list.append(mot_controller_task)
    
    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            #motor.disable()
            #servo.disable()
            IR_sens.disable()
            print("[Main] IR sensor disabled.")
            print("[Main] Motors disabled.")
            print("[Main] Exiting...")
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(comms_task.get_trace())
    print('')



    #E-stop needed for:

    # Motor errors from fault pin on motor driver
#     DRV8838 Fault Detection:
#       Use the FAULT pin to detect overcurrent (1.8A), thermal shutdown, or undervoltage conditions.
#       Monitor the FAULT pin in your motor class or task.
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
        #     # Kill pose (E-stop situation only), tilt head down and turn off motors
        #     print("State 7: Emergency stop activated. Shutting down motors and moving to Kill Pose.")

        #     # Disable motors and servo
        #     motor.disable()
        #     servo.write_angle(0)  # Move servo to Kill Pose (e.g., head tilted down)
        #     pyb.Pin('POWER_PIN', pyb.Pin.OUT).low()  # Replace 'POWER_PIN' with the actual pin controlling power

        #     print("Motors and servo disabled. System in Kill Pose.")
        #     yield state


    # Loss of communication with Bluetooth
    # Out of bounds positions for the servo or motor
    