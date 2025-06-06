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

class ButtonInterrupt(Exception):
    pass

button_pin = Pin('C3', Pin.IN, Pin.PULL_UP)

class SystemInitializer:
    def __init__(self, IR_sens, comms_state, ir_sensor_state, sensor_triggered, kill_message, uart, bluetooth):
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
        self.bluetooth = bluetooth  # Bluetooth UART
        self.bt_state_pin = Pin('B14', Pin.IN)
        self.uart = uart    

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
        
        # Wait for RSPI to be ready
        self.wait_for_rspi()

    def wait_for_bluetooth_connection(self):
        """Wait until a Bluetooth connection is established."""
        print("[Init] Checking Bluetooth connection...")
        while self.bt_state_pin.value() != 1:  # Repeat until the connection is established
            print("Waiting for Bluetooth connection...")
            pyb.delay(500)  # Wait for 500ms before checking again

        print("[Init] Bluetooth connected!")

    def wait_for_rspi(self):
        """Wait until the RSPI is ready."""
        print("[Init] Waiting for RSPI to be ready...")
        while True:
            line = self.uart.readline()
            if line:
                try:
                    msg = line.decode().strip()
                    if msg == 'IDLE':
                        break
                except Exception as e:
                    print("UART decode error:", e)
            print("Waiting for RSPI to be ready...")
            pyb.delay(500)
    # def zero_encoder(self):
    #     """Zero the encoder."""
    #     self.encoder.zero()
    #     print("[Init] Encoder zeroed.")

    # def initialize_motor(self):
    #     """Initialize the motor."""
    #     self.motor.disable()
    #     print("[Init] Motor initialized and disabled.")
    
    def initialize_IR_sensor(self):
        """Initialize the IR sensor."""
        self.IR_sens.enable()
        self.sensor_triggered.put(0)  # Reset the sensor trigger flag
        self.kill_message.put(0)  # Reset the KILL message flag
        print("[Init] IR sensor initialized and enabled.")

    # def initialize_servo(self):
    #     """Initialize the servo."""
    #     #self.servo.enable()
    #     print("[Init] Servo initialized and disabled.")


if __name__ == "__main__":
    # Create instances of the encoders, motors, and servos
    #encoder = Encoder(3, 'A6', 'A7')
    #motor = Motor(4, 1,'B6', 'C8', 'C7')
    #servo = Servo(2, 'A15')
    #controller = PIDController(10, 2, 0.02)
    IR_sens = MOT2002_IR('B1')
    uart = UART(3, baudrate=9600,timeout=1)
    bluetooth = UART(1, 115200, timeout=1000)


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
    # motion_profile = task_share.Share('h', thread_protect=False,
    #                                     name="motion_profile") 

    comms_state = task_share.Share('h', thread_protect=False,
                                        name="comms_state") 
    ir_sensor_state = task_share.Share('h', thread_protect=False,
                                        name="ir_sensor_state") 
    # motion_profile_state = task_share.Share('h', thread_protect=False,
    #                                     name="motion_profile_state")                                

# Initialize the system
    initializer = SystemInitializer(IR_sens, comms_state, ir_sensor_state, sensor_triggered, kill_message, uart, bluetooth)

# Create the tasks.

    comms_task = cotask.Task(comms, name="comms", priority=1, period=50,
                            profile=True, trace=False, 
                            shares=(comms_state, comm_message, kill_message, 
                                    bluetooth, uart, sensor_triggered)) 

    IR_sensor_task = cotask.Task(IR_sensor, name="IR_sensor", 
                         priority=2, period=100, profile=True, trace=False,
                         shares = (sensor_triggered, ir_sensor_state, 
                                   IR_sens, kill_message, comm_message))
    # motion_profile_task = cotask.Task(motion_profiles, name="motion_profiles",
    #                      priority=2, period=22, profile=True, trace=False,
    #                      shares = (motion_profile_state, motion_profile, kill_message, servo, comm_message))
    

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
            if button_pin.value() == 0:  # Active-low: pressed when 0
                raise ButtonInterrupt
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            uart.write('KILL'.encode())
            bluetooth.write('8'.encode())
            IR_sens.disable()
            print("[Main] IR sensor disabled.")
            #print("[Main] Motors disabled.")
            print("[Main] Exiting...")
            break
        except ButtonInterrupt:
            IR_sens.disable()
            uart.write('KILL'.encode())
            bluetooth.write('8'.encode())
            print("[Main] IR sensor disabled.")
            #print("[Main] Motors disabled.")
            print("[Main] Emergency stop: Button pressed. Exiting...")
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(comms_task.get_trace())
    print('')

    