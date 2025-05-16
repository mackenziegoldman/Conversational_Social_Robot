# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

import pyb
from pyb import Pin, UART
import cotask
import task_share 


def comms(shares):
    """USB communication task for user interaction."""
    comms_state, comm_message, kill_message, bluetooth = shares
    state = comms_state.get()
    message = None  # Initialize message variable
    send_message = None  # Initialize send_message variable
    uart = UART(3, baudrate=9600)

    while True:
        #print(f"[Sensor Task] Queue size after put: {comm_message.num_in()}")
        state = comms_state.get()
        if state == 1: #"WAIT"
            if uart.any():
                comms_state.put(3) # Set state to RECEIVE
            elif not comm_message.empty():
                send_message = comm_message.get()
                print(f"Message Code to send: {send_message}")
                comms_state.put(2) # Set state to SEND
            else:
                print("No data to send or receive.")
                comms_state.put(1) # Stay in WAIT state
            yield state

        elif state == 2: #"SEND"
            try:
                if send_message < 3:  # Check if there is a message to send
                    if send_message == 1:
                        message = "START"
                        uart.write(message.encode())  # Send the message via UART
                        print(f"Sent: START")
                    elif send_message == 2:
                        message = "KILL"
                        uart.write(message.encode())  # Send the message via UART
                        print(f"Sent: KILL")
                        comm_message.put(8) # Send KILL message to phone
                    send_message = None  # Clear the message after sending
                    comms_state.put(1)  # Go back to WAIT state
                elif send_message >= 3:
                    bluetooth.write(f"{send_message}\n")
                    print(f"Sent: {send_message}")
                    comms_state.put(1)  # Go back to WAIT state
                    send_message = None
            except Exception as e:
                print(f"Error: Failed to send message. {e}")
                comms_state.put(1)
            yield state

        elif state == 3: #"RECEIVE"
            try:
                line = uart.readline()  # Read a line from UART
                if line:
                    try:
                        message = line.decode().strip()  # Decode the received message
                        print("Received: ", message)
                        # Process the received message
                    except UnicodeDecodeError:
                        print("Error: Failed to decode UART message.")
                        comms_state.put(1)  # Return to WAIT state
                        continue
                else:
                    print("Warning: No data received from UART.")
                    comms_state.put(1)  # Return to WAIT state
                    continue
            except Exception as e:
                print(f"Error: UART communication failed. {e}")
                comms_state.put(1)  # Return to WAIT state
                continue

            if message == "IDLE":
                comm_message.put(3)
                comms_state.put(1)
                #send message to phone 
            elif message == "KILL":
                #####shutdown the robot
                #send a message to the phone
                comm_message.put(8)
                comms_state.put(1)
                kill_message.put(1)
            elif message == "HAPPY":
                #send message to phone and possible motion for it?
                comm_message.put(4)
                comms_state.put(1)
            elif message == "THINKING":
                #send message to phone and possible motion for it?
                comm_message.put(5)
                comms_state.put(1)
            elif message == "TALKING":
                #send message to phone
                comm_message.put(6)
                comms_state.put(1)
            elif message == "LISTENING":
                #send message to phone
                comm_message.put(7)
                comms_state.put(1)
            else:
                print("Unknown command received")
            yield state


#send_message Key:

# 1 = START (STM32 -> Raspberry Pi)
# 2 = KILL (STM32 -> Raspberry Pi)

# 3 = IDLE (STM32 -> phone)
# 4 = HAPPY (STM32 -> phone)
# 5 = THINKING (STM32 -> phone)
# 6 = TALKING (STM32 -> phone)
# 7 = LISTENING (STM32 -> phone)
# 8 = KILL (STM32 -> phone)

# bt_state_pin = Pin('X1', Pin.IN)  # Replace 'X1' with the actual pin connected to the STATE pin

# def is_bluetooth_connected():
#     """Check if the Bluetooth module is connected."""
#     return bt_state_pin.value() == 1  # 1 indicates connection

# def comms(shares):
#     """USB communication task for user interaction."""
#     comms_state, comm_message, kill_message = shares
#     state = comms_state.get()
#     message = None  # Initialize message variable
#     send_message = None  # Initialize send_message variable
#     uart = UART(3, baudrate=9600)
#     bluetooth = UART(1, 115200, timeout=1000)  # Bluetooth UART

#     while True:
#         state = comms_state.get()

#         # Check Bluetooth connection status
#         if not is_bluetooth_connected():
#             print("Bluetooth connection lost!")
#             comm_message.put(8)  # Send KILL message to phone
#             kill_message.put(1)  # Trigger emergency stop
#             comms_state.put(1)  # Return to WAIT state

#         # Handle other states...
#         yield state