# Code written by: Mackenzie Goldman, EIT for Conversational Social Robot
# ME Senior Design Project 2024-2025

from pyb import Pin, Timer

class Servo:
    
    def __init__(self, pin_servo, freq=50, min_ms=1, max_ms=2, angle=90):
        self.freq = freq
        self.min_ms = min_ms
        self.max_ms = max_ms
        self.angle = angle
        self.timer = Timer(2, freq=freq)
        self.channel = self.timer.channel(1, Timer.PWM, pin=Pin(pin_servo))
        print(f"Servo initialized on pin {pin_servo} with freq {freq}")

    def write_ms(self, ms):
        if ms < self.min_ms:
            ms = self.min_ms
        elif ms > self.max_ms:
            ms = self.max_ms
        duty_cycle = (((ms/1000)/(1/self.freq))*100)  # calculation for duty cycle
        self.channel.pulse_width_percent(duty_cycle)  # Convert to percentage
        print(f"Set pulse width to {ms} ms (duty cycle: {duty_cycle}%)")

    def write_angle(self, angle_in):
        if angle_in < 0:
            angle_in = 0
        elif angle_in > self.angle:
            angle_in = self.angle
        ms = self.min_ms + ((self.max_ms - self.min_ms) / self.angle) * angle_in
        self.write_ms(ms)
        print(f"Set angle to {angle_in} degrees (pulse width: {ms} ms)")

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

    current_angle = self.get_current_angle()
    step = 1 if target_angle > current_angle else -1

    while current_angle != target_angle:
        current_angle += step * speed
        if (step > 0 and current_angle > target_angle) or (step < 0 and current_angle < target_angle):
            current_angle = target_angle  # Ensure we don't overshoot the target

        self.write_angle(current_angle)
        yield  # Yield control to allow other tasks to run

def get_current_angle(self):
    """
    Placeholder for getting the current angle.
    In a real implementation, this would track the last set angle.
    """
    # For now, assume the last set angle is stored in self.current_angle
    return getattr(self, "current_angle", 0)

def predict_velocity(self, speed, delay_ms):
    """
    Predict the velocity of the servo in degrees per second.
    :param speed: Step size in degrees per iteration.
    :param delay_ms: Delay between iterations in milliseconds.
    :return: Predicted velocity in degrees per second.
    """
    delay_seconds = delay_ms / 1000  # Convert milliseconds to seconds
    velocity = speed / delay_seconds
    print(f"Predicted Velocity: {velocity} degrees/second")
    return velocity




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