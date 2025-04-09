from time import ticks_ms, ticks_diff, ticks_add
from pyb import Pin, Timer

class Encoder:
    '''A quadrature encoder decoding interface encapsulated in a python class'''

    def __init__(self, tim, chA_pin, chB_pin):
        '''Initializes an Encoder object'''

        self.position   = 0 #total accumulated position of the encoder
        self.prev_count = 0 #counter value from the most recent update
        self.delta      = 0 #change in count between last two updates
        self.dt         = 0 #amount of time between last two updates

        # copy params to attrbutes
        self.tim = tim
        self.chA_pin = chA_pin
        self.chB_pin = chB_pin

        # Configure timer channels for encoder interface
        self.Timer(self.tim, prescaler=0, period=0xFFFF)
        self.tim.channel(1, pin=self.chA_pin, mode=Timer.ENC_AB)
        self.tim.channel(2, pin=self.chB_pin, mode=Timer.ENC_AB)


    def update(self):
        '''Runs one update step on the encoder's timer counter to keep track of 
        the change in count and check for counter reload'''
        #get current count
        self.dt = 100_000 # 100ms
        start = ticks_ms()
        deadline = ticks_add(start, self.dt)
        while True:
            now = ticks_ms()
            if ticks_diff(deadline, now) >= 0:
                # update for overflow/underflow
                count = self.tim.counter()
                self.delta = self.prev_count - count
                self.prev_count = count
                if self.delta >= 32768: #AR+1/2 
                    self.delta = self.delta - 65536
                elif self.delta <= -32768:
                    self.delta = self.delta + 65536
                self.position = self.position + self.delta
                deadline = ticks_add(deadline, self.dt)

    def get_position(self):
        '''Returns the most recently updated value of position as determined 
        within the update() method'''
        return self.position
        
    def get_velocity(self):
        '''Returns a measure of velocity using the most recently updated value 
        of delta as determined within the update() method'''
        return self.delta/self.dt
    
    def zero(self):
        '''Sets the present encoder position to zero and causes future cupdates 
        to measure with respect to the new zero position'''
        self.position   = 0
        self.delta      = 0
        self.prev_count = 0
