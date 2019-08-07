# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 21:20:10 2018

@author: aidam
"""

import pyb
from pyb import Pin, Timer, ADC, UART, LED, delay
print('Task 9: Keypad controlling motor')

#initialise UART communication
uart = UART(6)
uart.init(9600, bits=8, parity = None, stop = 2)
mode = 0
# set up motor with PWM and timer control
A1 = Pin('Y3',Pin.OUT_PP) # motor 1
A2 = Pin('Y4',Pin.OUT_PP)
pwm_out1 = Pin('Y9')

B1 = Pin('Y5', Pin.OUT_PP) # motor 2
B2 = Pin('Y6', Pin.OUT_PP)
pwm_out2 = Pin('Y10')

us = ADC(Pin("X5"))
sensor = us.read()
hs = Pin('X11', Pin.IN)

RED = LED(1)
GREEN = LED(2)
YELLOW = LED(3)
BLUE = LED(4)


IR_sensor1 = Pin('X10', Pin.IN)
IR_sensor2 = Pin('X9', Pin.IN)

tim = Timer(2, freq = 1000)
motor1 = tim.channel(3, Timer.PWM, pin = pwm_out1)
motor2 = tim.channel(4, Timer.PWM, pin = pwm_out2)


# Motor in idle state
A1.high()
A2.high()
B1.high()
B2.high()
#_____________________________________________________________________________
# Use keypad U and D keys to control speed
while True:
	if uart.any() >= 10:
		command = uart.read(10)
		command2 = uart.read(20)
		print(command)

#_____________________________________________________________________________
		if command[2] == ord('1'):
			mode = 1
			print('mode 1')

		elif command[2] == ord('2'):
			mode = 2
			print('mode 2')

		elif command[2] == ord('3'): #shootout
			mode = 3
			print('mode 3')

#_____________________________________________________________________________
	if mode == 1:
		print('roaming activated')		#infrared
		if IR_sensor1.value() and IR_sensor2.value(): #no value
			RED.off()
			A1.high()
			A2.low()
			B1.low()
			B2.high()
			motor1.pulse_width_percent(50)
			motor2.pulse_width_percent(50)

		elif IR_sensor1.value() == 1:
			RED.on()
			print('LEFT')
			motor1.pulse_width_percent(0)
			motor2.pulse_width_percent(80)

		elif IR_sensor2.value() == 1:
			RED.on()
			print('RIGHT')
			motor1.pulse_width_percent(80)
			motor2.pulse_width_percent(0)

		else:
			motor1.pulse_width_percent(0)
			motor2.pulse_width_percent(0)
#_____________________________________________________________________________
	elif mode == 2:
		print('controls activated')
		if command[2]==ord('5'): # up
			print('up')
			A1.high()
			A2.low()
			B1.low()
			B2.high()
			motor1.pulse_width_percent(70)
			motor2.pulse_width_percent(70)

		elif command[2]==ord('6'): # down
			print('down')
			A1.low()
			A2.high()
			B2.low()   
			B1.high()
			motor1.pulse_width_percent(50)
			motor2.pulse_width_percent(50)

		elif command[2]==ord('7'): # left
			print('left')
			B1.low()
			B2.high()
         A1.low() #maybe take this out
			A2.high() #possibly will work
			motor1.pulse_width_percent(50) #if fails set to 0
			motor2.pulse_width_percent(50)

		elif command[2]==ord('8'):
			print('right')
			A2.low()		# right
			A1.high()
         B2.low()   #maybe take this out
			B1.high() #possibly wrong
			motor1.pulse_width_percent(50)
			motor2.pulse_width_percent(50) #if it does not work set to 0

		elif command[2]==ord('4'):# stop
			print('stop')
			A1.low()
			A2.low()
			B2.low()
			B1.low()
			motor1.pulse_width_percent(0)
			motor2.pulse_width_percent(0)
        
        
			if IR_sensor1.value()==0 or IR_sensor2.value()==0:
				print('inert rock! = YELLOW')
				YELLOW.on()
            
         elif sensor >= 2000:
             RED.on()
             print("the car is close, ULTRASOUND ROCK = RED")
             print(us.read())
             delay(100)
             
         elif hs.value() == 0:
            BLUE.on()
            
        