import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)

dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13
levels = 2**len(dac)


GPIO.setup(dac,GPIO.OUT)
GPIO.setup(troyka,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]


def adc():
    for i in range(256):
        time.sleep(0.05)
        b = decimal2binary(i)
        GPIO.output(dac, b)
        compvalue = GPIO.input(comp)
        if(compvalue == 0):
            return i


def num2dac (value):
    signal = decimal2binary(value)   
    GPIO.output(dac,signal)  
    return signal       
            
 
try:
    while True:
        for value in range(256):
            time.sleep(0.0005)
            signal = num2dac (value)
            voltage = value/levels *3.3
            compvalue = GPIO.input(comp)
            if(compvalue == 1):
                print("ADC value = {:^3} -> {}, input voltage = {:.2f}".format(value,signal, voltage) )      
                break
    

finally: 
    GPIO.output(dac, 0)
    GPIO.cleanup()