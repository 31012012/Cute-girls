import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
dac = [8,11,7,1,0,5,12,6]

GPIO.setup(dac,GPIO.OUT, initial = GPIO.HIGH)

p = GPIO.PWM(23,1000)
p.start(0)
 
try:
    while True:
        DutyCycle = int(input())
        p.ChangeDutyCycle(DutyCycle)       
        print("{:.2f}".format(DutyCycle*3.3/100)) 

       
    

finally: 
    GPIO.output(23, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()