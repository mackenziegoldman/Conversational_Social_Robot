from pyb import Pin, Timer, ADC
import time

class QTR_HD_15A:
    def __init__(self, adc_pins, num_sensors, power_odd, power_even):
        """
        Initialize the QTR-HD-15A reflectance sensor array.
        :param adc_pins: List of ADC-capable pin names (e.g., ['X1', 'X2', ...])
        :param num_sensors: Number of sensors in the array (default 15).
        """
        if len(adc_pins) != num_sensors:
            raise ValueError("Number of ADC pins must match the number of sensors")

        self.num_sensors = num_sensors
        self.adc_pins = adc_pins
        self.adc_channels = [ADC(Pin(pin)) for pin in adc_pins]
        self.enabled = False
        self.power_odd = Pin(power_odd, Pin.OUT_PP) # Power pin for odd sensors
        self.power_even = Pin(power_even, Pin.OUT_PP)  # Power pin for even sensors
        self.calibrated_min = [4095] * num_sensors  # Assuming 12-bit ADC
        self.calibrated_max = [0] * num_sensors
        self.disable  # Sensor is initially disabled

    def enable(self):
        """Enable the sensor."""
        self.power_odd.high()
        self.power_even.high()  # Turn on power to the sensors
        self.enabled = True

    def disable(self):
        """Disable the sensor."""
        self.power_odd.low()
        self.power_even.low()  # Turn off power to the sensors
        self.enabled = False

    def read_raw(self):
        """
        Read raw values from the sensor array.
        :return: List of raw ADC values.
        """
        if not self.enabled:
            print("Sensor is disabled. Cannot read raw values.")
            return [0] * self.num_sensors

        values = [adc.read() for adc in self.adc_channels]
        return values

    def calibrate_light(self, num_samples=100):
        """
        Calibrate the sensor by finding min/max values over multiple samples.
        :param num_samples: Number of calibration cycles.
        """
        if not self.enabled:
            print("Sensor is disabled. Cannot calibrate.")
            return

        print("Starting calibration light...")
        time.sleep_ms(3000)
        for _ in range(num_samples):
            values = self.read_raw()
            for i in range(self.num_sensors):
                if values[i] < self.calibrated_min[i]:
                    self.calibrated_min[i] = values[i]
                if values[i] > self.calibrated_max[i]:
                    self.calibrated_max[i] = values[i]
            time.sleep_ms(10)
        print("Calibration light complete.")

    def calibrate_dark(self, num_samples=100):
        """
        Calibrate the sensor by finding min/max values over multiple samples for a dark background.
        :param num_samples: Number of calibration cycles.
        """
        if not self.enabled:
            print("Sensor is disabled. Cannot calibrate.")
            return

        print("Starting calibration dark...")
        time.sleep_ms(3000)
        for _ in range(num_samples):
            values = self.read_raw()
            for i in range(self.num_sensors):
                if values[i] < self.calibrated_min[i]:
                    self.calibrated_min[i] = values[i]
                if values[i] > self.calibrated_max[i]:
                    self.calibrated_max[i] = values[i]
            time.sleep_ms(10)
        print("Calibration dark complete.")

    def read_calibrated(self):
        """
        Read calibrated sensor values (scaled between 0 and 1000).
        :return: List of calibrated values.
        """
        if not self.enabled:
            print("Sensor is disabled. Cannot read calibrated values.")
            return [0] * self.num_sensors

        raw_values = self.read_raw()
        calibrated_values = []
        for i in range(self.num_sensors):
            value = raw_values[i]
            min_val = self.calibrated_min[i]
            max_val = self.calibrated_max[i]

            # Avoid division by zero
            if max_val - min_val == 0:
                calibrated_values.append(0)
            else:
                scaled_value = (value - min_val) * 1000 // (max_val - min_val)
                scaled_value = max(0, min(1000, scaled_value))
                calibrated_values.append(scaled_value)

        return calibrated_values

    def read_line_position(self):
        """
        Determine the position of the line (weighted average of sensor indices).
        :return: Line position as a float (0 to num_sensors - 1).
        """
        if not self.enabled:
            print("Sensor is disabled. Cannot read line position.")
            return (self.num_sensors - 1) / 2  # Default to center if sensor is disabled

        calibrated_values = self.read_calibrated()
        weighted_sum = 0
        sum_values = 0

        for i in range(self.num_sensors):
            weighted_sum += calibrated_values[i] * i
            sum_values += calibrated_values[i]

        if sum_values == 0:
            return (self.num_sensors - 1) / 2  # Default to center if no line is detected

        return weighted_sum / sum_values