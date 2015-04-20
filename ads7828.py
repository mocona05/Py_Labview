# -*- coding: utf-8 -*-
import smbus
import time

DEVICE_ADDRESS = 0x48      #7 bit address (will be left shifted to add the read write bit)
I2C_CHANNEL = 1  #raspberry i2c channel

PULL_UP_RESIST =41.2
PULL_DOWN_RESIST =10.0
ADC_REF_VOLT =5.0
DEFAULT_RATIO =1.0
ADC_RESOLUTION =4095.0

#TC1047 temperature sensor
TC1047_ZERO_DEGC =0.5
TC1047_DEGC_FOR_VOLT =0.01
#LM61B temperatur sensor
LM61B_ZERO_DEGC =0.6
LM61B_DEGC_FOR_VOLT =0.01

# temperature sensor set
ZERO_DEG = TC1047_ZERO_DEGC
DEGC_FOR_VOLT = TC1047_DEGC_FOR_VOLT

#ADC7828 CONTROL REGISTER
ADS7828_CONFIG_SD_DIFFERENTIAL      = 0x00
ADS7828_CONFIG_SD_SINGLE            = 0x80
ADS7828_CONFIG_CS_CH0               = 0x00
ADS7828_CONFIG_CS_CH1               = 0x40
ADS7828_CONFIG_CS_CH2               = 0x10
ADS7828_CONFIG_CS_CH3               = 0x50
ADS7828_CONFIG_CS_CH4               = 0x20
ADS7828_CONFIG_CS_CH5               = 0x60
ADS7828_CONFIG_CS_CH6               = 0x30
ADS7828_CONFIG_CS_CH7               = 0x70
ADS7828_CONFIG_PD_OFF               = 0x00
ADS7828_CONFIG_PD_REFOFF_ADON       = 0x04
ADS7828_CONFIG_PD_REFON_ADOFF       = 0x08
ADS7828_CONFIG_PD_REFON_ADON        = 0x0c

#ADS 7828 I2C CONTROL CLASS
class Ads7828:
    def __init__(self, address=DEVICE_ADDRESS, bus_id=I2C_CHANNEL, debug=False):
        self.i2c = smbus.SMBus(bus_id)
        self.address = address
        self.debug = debug
    def read_raw_adc(self, ch):
        config = 0
        config |= ADS7828_CONFIG_SD_SINGLE
        config |= ADS7828_CONFIG_PD_REFOFF_ADON
        if ch == 0:
            config |= ADS7828_CONFIG_CS_CH0
        elif ch == 1:
            config |= ADS7828_CONFIG_CS_CH1
        elif ch == 2:
            config |= ADS7828_CONFIG_CS_CH2
        elif ch == 3:
            config |= ADS7828_CONFIG_CS_CH3
        elif ch == 4:
            config |= ADS7828_CONFIG_CS_CH4
        elif ch == 5:
            config |= ADS7828_CONFIG_CS_CH5
        elif ch == 6:
            config |= ADS7828_CONFIG_CS_CH6
        elif ch == 7:
            config |= ADS7828_CONFIG_CS_CH7
 
        time.sleep(0.01)#adc convertion time waiting
        data =[0,0]
        data = self.i2c.read_i2c_block_data(self.address,config,2)
        time.sleep(0.01)
        return ((data[0] << 8) + data[1])
    def all_ch_raw_adc_display(self):
        data= [0]*8
        for i in range (8) :
           data[i] = adc.read_raw_adc(i)
        print ("ch0=%d, ch1=%d, ch2=%d, ch3=%d, ch4=%d, ch5=%d, ch6=%d, ch7=%d"  %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))

#ADC CONVERTION CALCULATOR CLASS
class Voltage_cal(Ads7828):
    def __init__(self, address=DEVICE_ADDRESS, bus_id=I2C_CHANNEL, debug=False, vref=ADC_REF_VOLT,default_ratio=DEFAULT_RATIO, offset=0):
        Ads7828.__init__(self, address, bus_id, debug)
        self.adc_resol =ADC_RESOLUTION
        self.vref =vref
        self.ratio =[self.adc_resol/(default_ratio*self.vref)]*8
        self.offset =[offset]*8
        self.temp_offset =[0.0]*8
        self.temp_devider = [1.0]*8
        self.adc_ratio_int()
        Ads7828()
    def adc_ratio_int(self):
        self.temp_ratio(0) # ADC temperature sensor setting
        self.ratio_set(1,0,1) #direct input adc(none pull-up & pull-down resist)
        self.ratio_set(2,0,1) #direct input adc(none pull-up & pull-down resist)
        self.ratio_set(3,0,1) #direct input adc(none pull-up & pull-down resist)
        self.ratio_set(7,0,1) #direct input adc(none pull-up & pull-down resist)
        for i in range(4,7):
            self.ratio_set(i) #adc pull-up & pull-down resist ratio set

    def ratio_set(self, ch, PULL_UP_RESIST=PULL_UP_RESIST, PULL_DOWN_RESIST =PULL_DOWN_RESIST):     #channel pull-up/pull-down ratio set
        regSum = PULL_UP_RESIST+PULL_DOWN_RESIST
        self.ratio[ch] = self.adc_resol/((regSum/PULL_DOWN_RESIST)*self.vref)
        
    def temp_ratio(self, ch, v_for_deg=DEGC_FOR_VOLT, zero_for_volt=ZERO_DEG):
        self.temp_offset[ch] = zero_for_volt / self.vref * self.adc_resol 
        self.temp_devider[ch] = v_for_deg / self.vref * self.adc_resol 
        
    def read_voltage(self, ch):
        ch_value = self.read_raw_adc(ch)/self.ratio[ch]-self.offset[ch]
        return round(ch_value,2)

    def read_temp(self,ch):
        ch_value = (self.read_raw_adc(ch)-self.temp_offset[ch]) / self.temp_devider[ch]
        return  round(ch_value,2)   

    def all_ch_value_display(self):
        data= [0]*8
        data[0] = self.read_temp(0)
        for i in range (1, 8) :
           data[i] = self.read_voltage(i)
        print ("Temp=%2.2fdegC, ch1=%2.2fV, ch2=%2.2fV, ch3=%2.2fV, ch4=%2.2fV, ch5=%2.2fV, In V=%2.2fV, BAT V=%2.2fV"  
               %(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7]))

if __name__ =="__main__":
#    adc = Ads7828()
    adc_measu = Voltage_cal()
    while True:
#        adc.all_ch_raw_adc_display() 
        adc_measu.all_ch_value_display()


