# -*- coding: utf-8 -*-
import time
import ms5611
import ht_01s
import cal_o2
import multiprocessing
import threading
import datetime
import sys

ht01s = ht_01s.Ht_01s()
MS5611 = ms5611.Ms_5611()
ari_oxy =cal_o2.Oxy_air()

class Update_sensor:
#    def __init__(self):
    def sensor_update(self):
        press, temp1 = MS5611.baro_read()
        humi, temp2, status = ht01s.humi_temp_read()
        air_oxygen= ari_oxy.cal_oxygen(temp1, humi, press)
        data = ("Oxy=%2.2f%%, Humi=%4.2f%%, Temp1=%3.2fdegC, Press=%4.2fkPa, Temp2=%3.2fdegC, HT-01s status= %d" 
          %(air_oxygen, humi, temp1, press, temp2, status))
        return(data)

if __name__ =="__main__":
    read_sensor = Update_sensor()
    while True:
        print (read_sensor.sensor_update())
