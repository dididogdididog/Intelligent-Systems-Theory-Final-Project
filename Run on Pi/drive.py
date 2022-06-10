from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from time import sleep
import RPi.GPIO as GPIO

turnAngleOrigin = 0

servo_pin = 25
motor_control = 17
motor_pwm = 27

factory = PiGPIOFactory()
servo = Servo(servo_pin, pin_factory=factory)

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pwm, GPIO.OUT)
GPIO.setup(motor_control, GPIO.OUT)
GPIO.output(motor_control, True)
pi_pwm = GPIO.PWM(motor_pwm, 1000)
pi_pwm.start(100)


def ChangeSpeed(speed):
    pi_pwm.ChangeDutyCycle(100-speed)


def turn(turnAngle):
    servo.value = turnAngle-turnAngleOrigin
