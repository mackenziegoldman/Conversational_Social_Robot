from pyb import Pin, Timer

class Motor:
    '''A motor driver interface encapsulated in a Python class. Works with 
        motor drivers using seperate PWM and direction inputs such as the 
        DRV8838 drivers present on the Romi chassis from Pololu'''
    def __init__(self, timer_num, chnl , PWM_pin, DIR_pin, nSLP_pin):
        '''Initializes a Motor object'''
        self.chnl = chnl
        self.DIR = Pin(DIR_pin, mode=Pin.OUT_PP)
        self.nSLP = Pin(nSLP_pin, mode=Pin.OUT_PP)
        self.tim = Timer(timer_num,freq=20000)
        self.PWM  = self.tim.channel(self.chnl, Timer.PWM, pin=Pin(PWM_pin)) 

    def set_effort(self, effort):
        '''Sets the present effort requested from the motor based on an input 
        value between -100 and 100'''
        if effort < 0:
            self.DIR.low()
            self.PWM.pulse_width_percent(-effort)
        else:
            self.DIR.high()
            self.PWM.pulse_width_percent(effort)

    
    def enable(self):
        '''enables motor driver by taking it out of sleep mode into break 
        mode'''
        self.nSLP.high()

    def disable(self):
        '''disables motor driver by putting it into sleep mode'''
        self.nSLP.low()
