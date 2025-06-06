# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

from pyb import Pin, Timer

class Servo:
    
    def __init__(self, pin_servo, freq=50, min_us=740, max_us=2100, angle=180):
        self.freq = freq
        self.min_us = min_us
        self.max_us = max_us
        self.angle = angle
        self.timer = Timer(2, freq=freq)
        self.current_angle = 0
        self.channel = self.timer.channel(1, Timer.PWM, pin=Pin(pin_servo))
        print(f"Servo initialized on pin {pin_servo} with freq {freq}")

    def write_us(self, us):
        if us < self.min_us:
            us = self.min_us
        elif us > self.max_us:
            us = self.max_us
        period_us = int(1_000_000 / self.freq)
        duty_cycle = (us / period_us) * 100
        self.channel.pulse_width_percent(duty_cycle)
        print(f"Set pulse width to {us} us (duty cycle: {duty_cycle}%)")

    def write_angle(self, angle_in):
        if angle_in < 0:
            angle_in = 0
        elif angle_in > self.angle:
            angle_in = self.angle
        us = self.min_us + ((self.max_us - self.min_us) / self.angle) * angle_in
        self.write_us(us)
        self.current_angle = angle_in  # Update the tracked angle
        print(f"Set angle to {angle_in} degrees (pulse width: {us} us)")

    def move_to(self, target_angle, speed=1):
        """
        Gradually move the servo to the target angle at the specified speed in a cooperative manner.
        :param target_angle: The desired angle to move to (0 to max angle).
        :param speed: Speed of movement in degrees per step (higher is slower).
        """
        if target_angle < 0:
            target_angle = 0
        elif target_angle > self.angle:
            target_angle = self.angle

        current_angle = self.current_angle  # Use the tracked angle
        step = 1 if target_angle > current_angle else -1

        while current_angle != target_angle:
            current_angle += step * speed
            if (step > 0 and current_angle > target_angle) or (step < 0 and current_angle < target_angle):
                current_angle = target_angle 

            self.write_angle(current_angle)
            yield  # Yield control to allow other tasks to run




# Example usage:

# # Initialize the servo
# servo = Servo(pin_servo='X1', freq=50, min_ms=1, max_ms=2, angle=180)

# # Predict the velocity
# speed = 2  # Degrees per step
# delay_ms = 20  # Delay between steps in milliseconds
# servo.predict_velocity(speed, delay_ms)

# # Start moving the servo
# move_task = servo.move_to(90, speed=speed)
# while True:
#     try:
#         next(move_task)  # Advance the servo movement
#         pyb.delay(delay_ms)  # Delay between steps
#     except StopIteration:
#         print("Servo movement complete")
#         break