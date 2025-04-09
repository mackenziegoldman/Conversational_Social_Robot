# STM Firmware Setup
If the STM32 Nucleo device is reset or a new device is used, the following steps will allow python to be run through the Shoe of Brian and on the STM32 board.

   1. Download the 'firmware.bin' file.
   2. Install the [STM Cube Programmer](https://www.st.com/en/development-tools/stm32cubeprog.html).
   3. Unplug the Nucleo from all power sources. 
   4. Move the jumper named JP5 from the "E5V" to the "U5V" position. That is, remove the small black rectangular shorting block and move it over one pin and reinsert it to short out the middle pin with "U5V" instead of "E5V".
   5. Connect the Nucleo to your computer with the ST-Link USB port, not the one on the Shoe of Brian.
   6. Open the STM Cube Programmer and select the 'firmware.bin' file.
   7. Press the "connect" button on the top right corner of the program. If this fails to connect its possible the board is damaged or you may have the jumper not set to "U5V".
   8. Occasionally software running on the Nucleo can lock out the ST-Link. If you think that may be the case, then attempt to connect several times while holding down the black reset button, releasing it approximately as you click on connect in the program.
   9. Once connected, press the button near the bottom left corner shaped like an eraser to perform a "full chip erase". If this step fails your Nucleo is most likely damaged.
   10. If the chip erase is successful, press the "download" button to flash the interpreter firmware.
   11. Once the programming is completed successfully, press the "disconnect" button in the programmer utility.
   12. Disconnect the USB cord from the ST-Link.
   13. Replace the jumper back on the "E5V" side so that you can use the Shoe of Brian once again.
   14. Confirm that you are able to access the REPL through PuTTY or any other serial communication port and that the PYBFLASH drive mounts properly.