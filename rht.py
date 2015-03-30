import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)  
import time

GPIO.setmode(GPIO.BCM)

rht_sensor_pin = 4
rht_input_set = GPIO.setup(rht_sensor_pin, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
rht_output_set = GPIO.setup(rht_sensor_pin, GPIO.OUT)

rht_pin_high = GPIO.output(rht_sensor_pin,True)
rht_pin_low = GPIO.output(rht_sensor_pin,False)

class rht_control :
    def __init__(self):
#        rht_output_set
        GPIO.setup(rht_sensor_pin, GPIO.OUT)
        rht_pin_high
    def sync_start(self):
        data_time = [0]*40
        start_time = time.time()
        rht_output_set
        rht_pin_low
        time.sleep(0.05)
#        GPIO.add_event_detect(rht_sensor_pin, GPIO.RISING)
#        rht_input_set        

        GPIO.setup(rht_sensor_pin, GPIO.IN)
        for i in range(5):
            GPIO.wait_for_edge(rht_sensor_pin, GPIO.RISING)
            start_time = time.time()
            GPIO.wait_for_edge(rht_sensor_pin, GPIO.POLING)
            data_time[i] = time.time()-start_time
        return data_time


if __name__ =="__main__":
    print "start!"
    rht_read = rht_control()
    print rht_read.sync_start()
    

#    while True:
