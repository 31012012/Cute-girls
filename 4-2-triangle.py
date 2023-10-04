import RPi.GPIO as GPIO
import sys
from time import sleep
dac = [8,11,7,1,0,5,12,6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]

 
try:
    while True:
        T = input()
        if not T.isdigit():
            print('Пожалуйста, введи число')
        t = int (T)/(510)
        for i in range(256):
            GPIO.output(dac, decimal2binary (i))
            print(decimal2binary (i))
            print (i)
            sleep(t)
        for i in range(255,-1,-1):
            GPIO.output(dac, decimal2binary (i))
            print(decimal2binary (i))
            print (i)
            sleep(t)

finally: 
    GPIO.output(dac, 1)
    GPIO.cleanup()