import pyb
import time

# Initialize UART3 with baud rate 9600 
# (using default pins PC4 for TX and PC5 for RX)
uart3 = pyb.UART(3, baudrate=9600)

while True:
    try:
        test_message = "START"
        uart3.write(test_message.encode())
        print("Sent: ", test_message)
        
        # Wait for a short period to allow the message to be received
        time.sleep(0.1)

        if uart3.any():
            line = uart3.readline()
            if line:
                try:
                    response = line.decode().strip()
                    print("Received: ", response)

                    if response == test_message:
                        print("Test passed")
                    else:
                        print("Test failed")
                except Exception as e:
                    print("Error decoding response: ", e)
            else:
                print("No data received")
        else:
            print("No data available")

        # Short delay to prevent flooding
        time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting...")
        break