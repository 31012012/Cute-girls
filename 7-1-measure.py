import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as ptl

GPIO.setmode(GPIO.BCM)


dac = [8,11,7,1,0,5,12,6]
led = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13

Maxvolt = 3.3
bit = len(dac)
levels = 2 ** bit

V = []
data_v = []
time_v = []

GPIO.setup(dac,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(troyka,GPIO.OUT)
GPIO.setup(led,GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)

def decimal2binary(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]
      

def adc(troyka):
    value = 0
    for i in range(7, -1, -1):
        b = decimal2binary(2 ** i  + value)
        GPIO.output(dac, b)
        time.sleep(0.005)   
        compvalue = GPIO.input(comp)
        if(compvalue == 0):
             value += 2**i
    return value
    



            
 
try:
    time_start  = time.time()
    count = 0
    voltage = 0

    #зарядка конденсатора
    GPIO.output(troyka,1)
    print ("Зарядка конденсатора")
    while (voltage <= 206):
        voltage = adc(troyka)
        print("Напряжение :", voltage/256 * Maxvolt)
        data_v.append(voltage/256 * Maxvolt) 
        time.sleep(0)
        count += 1
        b = decimal2binary(voltage)
        GPIO.output(led, b)
        time_v.append(time.time() - time_start )

    #разрядка конденсатора
    GPIO.output(troyka,0)
    print ("Разрядка конденсатора")
    while (voltage >= 177):
        voltage = adc(troyka)
        print("Напряжение :", voltage/256 * Maxvolt)
        data_v.append(voltage/256 * Maxvolt) 
        time.sleep(0)
        count += 1
        b = decimal2binary(voltage)
        GPIO.output(led, b)
        time_v.append(time.time() - time_start )
    
    time_end = time.time()
    time_total = time_end - time_start

    #выводим графики
    print("Графики")
    ptl.plot(time_v,data_v)
    ptl.xlabel("Секунды")
    ptl.ylabel("Напряжение") 
    print("Запись в файл")
    
    #заполняем текстовые файлы
    with open('data.txt','w') as f:
        for i in data_v:
            f.write(str(i) + '\n')

    with open('time.txt','w') as f:
        for i in time_v:
            f.write(str(i) + '\n')        

    with open('settings.txt','w') as f:
        f.write('Частота дискретизации = ' + str(1/time_total * count) + 'Гц' + '\n')
        f.write('Шаг квантования = 0.0129 В')
    print("Средняя частота дискретизации ", 1/time_total * count )     
    print("Общее время эксперимента",time_total )  
    print("Завершение программы")  


finally: 
    GPIO.output(dac, 0)
    GPIO.output(led, 0)
    GPIO.cleanup()
    ptl.show()
    