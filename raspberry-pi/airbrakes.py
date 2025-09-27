import time
import board
import pwmio
from adafruit_motor import servo

class Servo:
    """Controls the servo that opens and closes our air brakes"""
    
    def __init__(self, pin=18):
        """Set up the servo on the specified pin"""
        self.pwm = pwmio.PWMOut(getattr(board, f'D{pin}'), frequency=50)
        self.servo_motor = servo.Servo(self.pwm)
        
        # Start with brakes closed
        self.servo_motor.angle = 0
        print(f"Air brakes ready on pin {pin}")
    
    def open(self):
        """Deploy the air brakes to slow us down"""
        self.servo_motor.angle = 90
        print("Air brakes opened")
        time.sleep(0.5)
    
    def close(self):
        """Retract the air brakes completely"""
        self.servo_motor.angle = 0
        print("Air brakes closed")
        time.sleep(0.5)