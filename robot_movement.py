import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

GPIO.output(22,0)#jobb   hatra
GPIO.output(27, 0)#jobb elore
GPIO.output(5, 0)#bal hatra
GPIO.output(21,0)#bal elore

pj = GPIO.PWM(23, 50)
pb = GPIO.PWM(6, 50)
pj.start(0)
pb.start(0)



iranyok=[[27,21],[5,22],[21,22],[5,27]]#elore,hatra,jobbra,balra
bol=1

def frd(bol,irany,mertek):
	a=iranyok[irany][0]
	b=iranyok[irany][1]
	GPIO.output(a, 1)
	GPIO.output(b, 1)
	
	for i in range(mertek):
		pj.ChangeDutyCycle(100)
		pb.ChangeDutyCycle(88)
		time.sleep(0.1)

	GPIO.output(a,0)
	GPIO.output(b,0)

def fordul(irany,mertek):#2,3


	a=iranyok[irany][0]
	b=iranyok[irany][1]

	GPIO.output(a, 1)
	GPIO.output(b, 1)

	for i in range(mertek):
		pj.ChangeDutyCycle(80)
		pb.ChangeDutyCycle(70)
		time.sleep(0.1)

	GPIO.output(a, 0)
	GPIO.output(b, 0)

