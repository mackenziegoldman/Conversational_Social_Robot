# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

from pyb import Pin, ADC

class MOT2002_IR:
    def __init__(self, data_pin):
        """
        Initialize the MOT2002 IR sensor.
        :param data_pin: ADC-capable pin name (e.g., 'X1', 'X2', ...).
        """
        self.adc = ADC(Pin(data_pin))  # Initialize ADC channel for the data pin
        self.adc_max = 4095  # Assuming 12-bit ADC
        self.adc_min = 0
        self.enabled = False  # Sensor is initially disabled

    def enable(self):
        """Enable the sensor (logical enable)."""
        self.enabled = True

    def disable(self):
        """Disable the sensor (logical disable)."""
        self.enabled = False

    def read_raw(self):
        """
        Read the value from the IR sensor.
        :return: Sensor value (ADC reading).
        """
        if not self.enabled:
            raise RuntimeError("Sensor is disabled. Enable the sensor before reading.")
        
        raw_value = self.adc.read() # Read the ADC value
        return raw_value

    def logical_value(self):
        """
        Determine the logical value from the IR sensor reading.
        :return: Logical sensor value (either logical true (1) or false (0)).
        """
        if not self.enabled:
            raise RuntimeError("Sensor is disabled. Enable the sensor before reading.")
        raw_value = self.read_raw()
        voltage = (raw_value / self.adc_max) * 5  # Convert ADC value to voltage (5V is reference voltage)
        #print(f"Voltage: {voltage}V")
        max_val = 5 # Reference voltage range (0V to 5V)
        if voltage >= max_val - 4.5:
            return 1  # Logical true
        else: 
            return 0