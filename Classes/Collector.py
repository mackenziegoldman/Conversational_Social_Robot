# Purpose: A data collector class that interfaces with an encoder class
# to collect data

from array import array

class Collector:
    '''A data collector class that interfaces with an ADC to collect data'''
    def __init__(self):
        '''Initializes a Collector object'''
        self.data = [array('H', [0]*2000) for k in range(2)]
        self.idx = 0

    def collect(self, pos_value, vel_value):
        '''Collects position data in an array'''
        if self.idx < 2000:
            self.data[0][self.idx] = pos_value
            self.data[1][self.idx] = vel_value
            self.idx += 1

    def print_data(self):
        '''Prints the collected data as columns for position and velocity'''
        for x, value in enumerate(self.data):
          self.dt = 1/100_000 # 100 kHz sampling frequency, so 100 ms interval
          time_in_seconds = x * self.dt
          print(f"{time_in_seconds},{self.data[0][x]},{self.data[1][x]}")
