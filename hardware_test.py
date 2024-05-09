#
import time
import sys
import pigpio
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BCM)   # Set for broadcom numbering not board numbers...

pi_hw = pigpio.pi()   # connect to pi gpio daemon
dc = 3
in_dc = dc * 10000

# pi_hw.hardware_PWM(13, 50, 75000)  # 50 hz, 7.5 % duty cycle (1.5 msec)
##pi_hw.hardware_PWM(13, 50, 500000)  # 50 hz, 50 % duty cycle 

pi_hw.hardware_PWM(13, 50, in_dc)  # 1 MHz 50 % duty cycle 

time.sleep(5)

pi_hw.hardware_PWM(13, 0, 0)  # 0 hz, 0 % duty cycle - stop the motor! 
pi_hw.stop() # close pi gpio PWM resources