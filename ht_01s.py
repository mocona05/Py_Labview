# -*- coding: utf-8 -*-
import smbus
import time


I2C_CHANNEL = 1  #raspberry i2c channel
HT_01S_ADDRESS =0x28 #(7bit)
HT_01S_CONVERSION_TIME=0.25
HT_01S_CONVERTER_START_REGISTE    = 0


class Ht_01s:
    i2c = None
    data =[0,0,0,0]
 
    def __init__(self, address, busId, debug=False):
        self.i2c = smbus.SMBus(busId)
        self.address = address
        self.debug = debug
 
    def adc_read(self):
        self.i2c.write_byte(self.address, HT_01S_CONVERTER_START_REGISTE)
        time.sleep(HT_01S_CONVERSION_TIME)
        self.data = self.i2c.read_i2c_block_data(self. address,0xFF,4)
        return self.data
    def read_humidity(self):
        humidity = ((((self.data[0]&0x3F)<<8) + self.data[1])/163.84)
        return round(humidity,2)
    def read_temp(self):
#        temp = float(self.data[2]*64 + ((self.data[3]&0xFC)>>2))/16384*165-40
        temp = (self.data[2]*64 + ((self.data[3]&0xFC)>>2))/16384.0*165-40
        return round(temp,2)
    def read_status(self):
        status = ((self.data[0]&0xC0)>>6)
        return status
    def read_sensor(self):
        self.adc_read()
        self.humidity = self.read_humidity()
        self.temperature =self.read_temp()
        self.sensor_status = self.read_status()
        
    def display(self):
#        ht01s = Ht_01s(HT_01S_ADDRESS,I2C_CHANNEL,True)
        self.read_sensor()
#        print("Humidity =%3.2f%%, Temperatur =%3.2f degC" %(self.humidity,self.Temperature))
        print("Humidity =%4.2f %%, Temperature =%3.2f degC, status =%d" %(self.humidity,self.temperature, self.sensor_status))
#        print("%f" %self.humidity)
#       print("RAW DATA : " + str(raw_data))
#       print("RAW DATA = 0x%X 0x%X 0x%X 0x%X" %(raw_data[0], raw_data[1], raw_data[2], raw_data[3]))
    

ht01s = Ht_01s(HT_01S_ADDRESS,I2C_CHANNEL)
while True:   
#    HUMIDITY = Read_ht_01s(HT_01S_ADDRESS, I2C_CHANNEL)
    ht01s.display()
#    raw_data = ht01s.read_Data()
#    humidity = ht01s.read_humidity()
#    temperature = ht01s.read_Temp()
#    print("RAW DATA : " + str(raw_data))
#    print("RAW DATA = 0x%X 0x%X 0x%X 0x%X" %(raw_data[0], raw_data[1], raw_data[2], raw_data[3]))
#    print("Humidity =%3.2f" %humidity)
#    print("Temperatur =%3.2f" %temperature)
    
    
    