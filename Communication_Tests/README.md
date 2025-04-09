# Communication Tests

The following code was used for testing and initialization purposes for both the UART connection with the Raspberry Pi device and the bluetooth connection with the Android phone.

## UART
UART_ was tested utilizing a loopback test in 'main.py'. After UART_ was confirmed working, tests were performed between the Raspberry Pi and STM32 Nucleo boards to ensure communication. 

### Test description and results


## Bluetooth
The 'BT_confugurator.py' program was used to configure the HC-05 Bluetooth module. The program changes the standard baudrate of the device to 11500, sets the name of the bluetooth device and the password. If necessary, the following code could be implemented in this program to reconfigure the STM32 Nucleo's pins for a non-standard UART pin connection between the board and the bluetooth module.

<!-- insert code snippet here -->