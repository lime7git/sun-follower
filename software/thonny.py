from machine import Pin, PWM, ADC
from time import sleep


rotate = PWM(Pin(19))
decline= PWM(Pin(18))

MIN_DECLINE = 4200
MAX_DECLINE = 7400

MIN_ROTATE  = 1500
MAX_ROTATE  = 8000

rotate.freq(50)
decline.freq(50)
ADC_0 = ADC(Pin(26))
ADC_1 = ADC(Pin(27))
photo_res_1 = Pin(16, Pin.OUT)
photo_res_2 = Pin(17, Pin.OUT)
photo_res_3 = Pin(20, Pin.OUT)
photo_res_4 = Pin(21, Pin.OUT)
 
ph1=0
ph2=0
ph3=0
ph4=0
#histerese_in_%
histerese = 0.1

def mean_value(a,b,c,d):
    return (a+b+c+d)/4
    
def max_value(a,b,c,d):
    max = a
    if b>max: max =b
    if c>max: max =c
    if d>max: max =d
    return max

def min_value(a,b,c,d):
    min = a
    if b<min:  min =b
    if c<min:  min =c
    if d<min:  min =d
    return min


def read_ADC(photo_resostor_number):
    mean=0
    
    if photo_resostor_number == 1:
            photo_res_1.on()
            photo_res_2.off()
            photo_res_3.off()
            photo_res_4.off()
            sleep(0.001)
            for i in range (1,1000):
                mean+=ADC_0.read_u16()/1000
                
            return mean
        
    if photo_resostor_number == 2:
            photo_res_1.off()
            photo_res_2.off()
            photo_res_3.off()
            photo_res_4.on()
            sleep(0.001)
            for i in range (1,1000):
                mean+=ADC_0.read_u16()/1000
            return mean
        
    if photo_resostor_number == 3:
            photo_res_1.off()
            photo_res_2.off()
            photo_res_3.on()
            photo_res_4.off()
            sleep(0.001)
            for i in range (1,1000):
                mean+=ADC_1.read_u16()/1000
                
            return mean
    
    if photo_resostor_number == 4:
            photo_res_1.off()
            photo_res_2.on()
            photo_res_3.off()
            photo_res_4.off()
            sleep(0.001)
            for i in range (1,1000):
                mean+=ADC_1.read_u16()/1000
                
            return mean
    
def work_rotate (deg):
    
    work = (MAX_ROTATE - MIN_ROTATE)/180*(deg+90) + MIN_ROTATE
    if work > MAX_ROTATE: value = MAX_ROTATE
    if work < MIN_ROTATE: value = MIN_ROTATE
    rotate.duty_u16(int(work))
    return 0
def work_decline(deg):
   
    work = (-(MAX_DECLINE - MIN_DECLINE)/90*(deg-90)) + MIN_DECLINE
    if work > MAX_DECLINE: value = MAX_DECLINE
    if work < MIN_DECLINE: value = MIN_DECLINE
    decline.duty_u16(int(work))
    
    return 0 
    
work_decline(0)
work_rotate(0)
position_X=0.0
position_Y=0.0

def check_rotate(a,b,c,d):
    global histerese
    global position_X
    if (a+c-histerese) > (b+d):
        if position_X <  90:position_X -=1
    if (b+d-histerese) > (a+c):
        if position_X > -90:position_X +=1
    print('a+c',a+c,'   ?    b+d',b+d)
    return 0

def check_decline(a,b,c,d):
    global histerese
    global position_Y
    if (a+b-histerese) > (c+d):
        if position_Y <  90:position_Y +=1
    if (c+d-histerese) > (a+b):
        if position_Y >   0:position_Y -=1
    print('a+b',a+b,'   ?    c+d',c+d)
    return 0
while True:
    
    ph1=read_ADC(1)
    ph2=read_ADC(2)
    ph3=read_ADC(3)
    ph4=read_ADC(4)
    
    maximum = max_value(ph1,ph2,ph3,ph4)
    minimum = min_value(ph1,ph2,ph3,ph4)
    srednia = mean_value(ph1,ph2,ph3,ph4)
    rozstep = maximum - minimum
    
    histerese = 800
    
    check_rotate(ph1,ph2,ph3,ph4)
    check_decline(ph1,ph2,ph3,ph4)
    
    print('RES_1',ph1)
    print('RES_2',ph2)
    print('RES_3',ph3)
    print('RES_4',ph4)
    print('_______________')
    print('srednia',srednia)
    print('max    ',maximum)
    print('min    ',minimum)
    print('rozstep',rozstep)
    print('_______________')
    work_rotate(position_X)
    work_decline(position_Y)
    
    
    
    

