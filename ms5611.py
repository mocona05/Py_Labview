# -*- coding: utf-8 -*-
import smbus
import time


I2C_CHANNEL = 1  #raspberry i2c channel
CSB_LOW_ADDRESS =0x77 #(7bit)
CSB_HIHG_ADDRESS =0x76 #(7bit)
MS5611_CONVERSION_TIME=0.5
MS5611_RESET_WAIT_TIME=2.8

CMD_RESET           =   0x1E # ADC reset command
CMD_ADC_READ        =   0x00 # ADC read command
CMD_ADC_CONV        =   0x40 # ADC conversion command
CMD_ADC_D1          =   0x00 # ADC D1 conversion
CMD_ADC_D2          =   0x10 # ADC D2 conversion
CMD_ADC_256         =   0x00 # ADC OSR=256
CMD_ADC_512         =   0x02 # ADC OSR=512
CMD_ADC_1024        =   0x04 # ADC OSR=1024
CMD_ADC_2048        =   0x06 # ADC OSR=2048
CMD_ADC_4096        =   0x08 # ADC OSR=4096
CMD_PROM_RD         =   0xA0 # Prom read command
PROM_NB             =   8 #
CMD_OSR = CMD_ADC_4096      #adc遺꾪빐 �μ뿉 �곕씪��寃곗젙 �쒕떎.

pressure=0
temperature =0
raw_temp =0
raw_press =0

class Ms_5611:
    i2c = None
    data =[0,0,0]
    on_chip_rom =[0,0,0,0,0,0,0,0]
 
    def __init__(self, address = CSB_LOW_ADDRESS, busId = I2C_CHANNEL, debug=False):
        self.i2c = smbus.SMBus(busId)
        self.address = address
        self.debug = debug
        self.read_status =0
        self.init()
    def reset(self):
        self.i2c.write_byte(self.address,CMD_RESET)
        time.sleep(MS5611_RESET_WAIT_TIME)
    def read_prom(self, coef_num):
        self.data = self.i2c.read_i2c_block_data(self. address,CMD_PROM_RD + coef_num * 2 ,2)
        return (self.data[0]<<8)+self.data[1]
    def init(self):
        self.reset()
        for x in range(0, PROM_NB):
            self.on_chip_rom[x] = self.read_prom(x)
    def read_adc(self):
        self.data = self.i2c.read_i2c_block_data(self.address, CMD_ADC_READ, 3)
        return (self.data[0]<<16)+(self.data[1]<<8)+self.data[2]
    def start_update_temp(self):
        reg = CMD_ADC_CONV + CMD_ADC_D2 + CMD_OSR
        self.i2c.write_byte_data(self.address, reg, 1)# temperature conversion start 
    def start_update_press(self):
        reg = CMD_ADC_CONV + CMD_ADC_D1 + CMD_OSR
        self.i2c.write_byte_data(self.address, reg, 1) # Pressure conversion start
    def get_temp(self):
        self.raw_temperature = self.read_adc()
    def get_pressure(self):
        self.raw_pressure = self.read_adc()
    def baro_read(self):
#        if self.read_status ==0: #�대옒�ㅻ� 泥섏쓬 �몄텧��痢≪젙 �쒖옉 以�퉬
#            self.start_update_temp()
#            self.read_status =1
#            self.elapased_time=self.start_time=time.time()

#        self.elapased_time = time.time()-self.start_time
#        if self.elapased_time < MS5611_CONVERSION_TIME:
#            time.sleep(MS5611_CONVERSION_TIME-self.elapased_time)   #遺�”�쒓컙 留뚰땲 湲곕떎由곕떎.
            time.sleep(MS5611_CONVERSION_TIME)   #遺�”�쒓컙 留뚰땲 湲곕떎由곕떎.
            raw_temp = self.get_temp()
            self.start_update_press()
            time.sleep(MS5611_CONVERSION_TIME)
            raw_press = self.get_pressure()
            self.start_update_temp() #�ㅼ쓬 痢≪젙���꾪빐��誘몃━ �⑤룄媛�蹂�솚���꾩넚�쒕떎.
#            self.start_time=time.time() #痢≪젙 媛쒖떆�쒓컙��湲곕줉
            self.pressure, self.temperature = self.calculate()
            return (self.pressure , self.temperature)
            
    def calculate(self):
        dT = self.raw_temperature - self.on_chip_rom[5] * 256
        off = (self.on_chip_rom[2] << 16) + ((self.on_chip_rom[4] * dT) >> 7)
        sens = (self.on_chip_rom[1] << 15) + ((self.on_chip_rom[3] * dT) >> 8)
        temp = 2000 + ((dT * self.on_chip_rom[6]) >> 23)
        if temp < 2000: #temperature lower than 20degC
            delt = temp - 2000
            delt = 5 * delt * delt
            off -= delt >>1
            sens -= delt >>2            
            if temp < -1500:  # temperature lower than -15degC
                delt = temp + 1500
                delt = delt * delt
                off -= 7 * delt
                sens -= (11 * delt) >> 1
        press = (((long(self.raw_pressure) * sens) >> 21) - off) >> 15
        pressure =round(float(press)/100.0,2)
        temperature = round(float(temp)/100.0,2)
        return (pressure, temperature)
        
if __name__ =="__main__":
    press = Ms_5611()
#    press.init()
    while True:    
        air_pressure, air_temperature = press.baro_read()
        print("Air Pressure= %4.2fkPa, Air Temperatur= %3.2fdegC" %(air_pressure, air_temperature))

