import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)

dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13

GPIO.setup(dac,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]


def adc(troyka):
    k = 0
    for i in range(7,-1,-1):
        k += 2**i
        b = decimal2binary(k)
        GPIO.output(dac, b)
        time.sleep(0.008)
        compvalue = GPIO.input(comp)
        if(compvalue == 1):
            k-= 2**i
    return k


def num2dac (value):
    signal = decimal2binary(value)   
    GPIO.output(dac,signal)  
    return signal       
            
 
try:
    while True:
        print(decimal2binary(adc(troyka)), "{:.4f}".format(adc(troyka) / 256* 3.3 ))  

finally: 
    GPIO.output(dac, 0)
    GPIO.cleanup()