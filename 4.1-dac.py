import RPi.GPIO as GPIO
import sys
dac = [8,11,7,1,0,5,12,6]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]


try:
    while True:
        print('Пожалйста, введите число от 0 до 255')    
        a = input()
        if(a == 'q'):
            sys.exit()
        elif not a.isdigit():
            print('Введите другое число')    

        elif (int (a) > 255 or int (a) < 0):
            print("Обратите внимание, необходимо ввести число от 0 до 255") 
            GPIO.output(dac,0)   
        else:
            GPIO.output(dac, decimal2binary(int (a)))
            print("{:4f}".format(int(a)/256*3.3))

finally: 
    GPIO.output(dac, 0)
    GPIO.cleanup()