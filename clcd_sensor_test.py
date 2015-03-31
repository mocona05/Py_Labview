import ht_01s
import ms5611
import cal_o2
import i2c_lcd_smbus





if __name__ =="__main__":
    ht01s = ht_01s.Ht_01s()
    MS5611 = ms5611.Ms_5611()
    oxy = cal_o2.Oxy_air()
    clcd = i2c_lcd_smbus.i2c_lcd(0x27,1,2,1,0,4,5,6,7,3)
    clcd.clear()
    clcd.backLightOn()
    while True:
        pressure, temp1 = MS5611.baro_read()
        humi, temp2, status = ht01s.humi_temp_read()
        lcd_string1 = ("H=%2.2f,T=%2.2f" %(humi, temp1))
        lcd_string2 = ("P=%2.2f" %(pressure))
        clcd.setPosition(1,0)
        clcd.writeString(lcd_string1)
        clcd.setPosition(2,0)
        clcd.writeString(lcd_string2)
        print("Humi=%4.2f%%, Temp1=%3.2fdegC, Press=%4.2fkPa, Temp2=%3.2fdegC, HT-01s status= %d" 
          %(humi, temp2, pressure, temp2, status))

        
