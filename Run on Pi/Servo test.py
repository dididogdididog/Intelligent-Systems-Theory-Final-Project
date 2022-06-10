from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from time import sleep
import RPi.GPIO as GPIO

servo_pin=25
motor_control=17
motor_pwm=27

val=0
step=0.01
minval=-0.2
maxval=0.2

factory=PiGPIOFactory()
servo=Servo(servo_pin,pin_factory=factory)

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pwm,GPIO.OUT)
GPIO.setup(motor_control,GPIO.OUT)
GPIO.output(motor_control,True)
pi_pwm=GPIO.PWM(motor_pwm,1000)
pi_pwm.start(50)

start_time=time.time()

while True:
		sleep(0.05)
		#servo.value=val
		val+=step
		if val>maxval:
			step=-0.01
		elif val<minval:
			step=0.01
		if time.time()-start_time>5:
			break
GPIO.cleanup()

