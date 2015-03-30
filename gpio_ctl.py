# -*- coding: utf-8 -*-
import time
import RPi.GPIO as GPIO
from compiler.misc import set_filename
#
switch1_pin = 4
fet_ch1_pin = 22
fet_ch2_pin = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(switch1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fet_ch1_pin, GPIO.OUT)
GPIO.output(fet_ch1_pin, False)
GPIO.setup(fet_ch2_pin, GPIO.OUT)
GPIO.output(fet_ch2_pin, False)

class Gpio_contro:
    def __init__(self):
        self.befor_status =[False]*2
        self.latch=[0]*2
    def read_button_input(self):
        self.button1 = not GPIO.input(switch1_pin)
        return self.button1
    #버튼을 다시 누를 떄까지 이전 상태를 유지한다.
    def output_flip_flop(self, ch, input_status):
        if input_status ==0:
            self.latch[ch] =1
        if self.latch[ch]==1 and input_status == 1:
            if self.befor_status[ch] ==True:
                self.latch[ch] =0
                self.befor_status[ch] = False
                print("ch%d Staus Low!" %ch)
            else :
                self.latch[ch] =0
                self.befor_status[ch] = True
                print("ch%d Staus high!" %ch)
        return self.befor_status[ch]
        
    def set_fet_output(self,ch1, ch2):
        self.fet_ch1 = ch1
        self.fet_ch2 = ch2
        GPIO.output(fet_ch1_pin, self.fet_ch1)
        GPIO.output(fet_ch2_pin, self.fet_ch2)
        print("ch1=%d, ch2=%d " %(ch1, ch2))
    def read_fet_output(self):
        return (self.fet_ch1, self.fet_ch2)
            
if __name__ =="__main__":
    print "start!"
    io = Gpio_contro()
    befor_status =0
    output1 = output2 =False
    while True:
        button1 = io.read_button_input()
        output1 = io.output_flip_flop(0, button1)
        output2 =io.output_flip_flop(1, button1)
        io.set_fet_output(bool(output1), bool(output2)) #button input of fet output control
        time.sleep(0.1)