import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)

dac = [8,11,7,1,0,5,12,6]
led = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13

GPIO.setup(dac,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]

def  binLeds (value):
    for i in range(8,0,-1):
        if i*32 - 1 <= value:
            return decimal2binary(2**i - 1)
            
    return decimal2binary(0)        

def adc(troyka):
    value = 0
    for i in range(7,-1,-1):
        b = decimal2binary(2**i + value)
        GPIO.output(dac, b)
        time.sleep(0.0008)
    
        compvalue = GPIO.input(comp)
        if(compvalue == 0):
             value += 2**i
    return value
    
            
 
try:
    while True:
        GPIO.output(led, binLeds(adc(troyka)))

finally: 
    GPIO.output(dac, [0]*8)
    GPIO.cleanup()