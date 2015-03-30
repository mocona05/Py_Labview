from Tkinter import *
import time
import ads7828
#import adc_read
import serial
import pygame
import wx

usbport ='/dev/ttyAMA0'
uart=serial.Serial(usbport,115200)
pygame.mixer.init()

#i2c-bus adc(ads7828) set 
#ADS7828_ADDRESS =0x48 #(7bit)
#I2C_CHANNEL = 1  #raspberry i2c channel
#adc set
#PULL_UP_REG =41.2
#PULL_DOWN_REG =10.0
#ADC_REF_VOLT =5.0
#DEFAULT_RATIO =1.0

#temperature sensor set
#TC4047_ZERO_DEGC =0.5
#TC4047_DEGC_FOR_VOLT =0.01

#adc = ads7828.ADS7828(ADS7828_ADDRESS, 1, True)

#ADC = adc_read.Voltage_cal(ADS7828_ADDRESS, I2C_CHANNEL, ADC_REF_VOLT,DEFAULT_RATIO,0 )
#ADC.tempRatio(TC4047_DEGC_FOR_VOLT, TC4047_ZERO_DEGC, 0)
#ADC.ratioSet(PULL_UP_REG,PULL_DOWN_REG,4)
#ADC.ratioSet(PULL_UP_REG,PULL_DOWN_REG,5)
#ADC.ratioSet(PULL_UP_REG,PULL_DOWN_REG,6)

adc_init = ads7828.Ads7828()
adc = ads7828.Voltage_cal()
class Application(wx.Frame):
   def __init__(self, parent): 
        wx.Frame.__init__(self, parent, -1, 'Raspberry Monitor', size=(180, 100)) 
        panel = wx.Panel(self) 
        sizer = wx.BoxSizer(wx.VERTICAL) 
        panel.SetSizer(sizer) 
        self.txt = wx.StaticText(panel, -1, 'temp',(10,10)) 
        self.txt2 = wx.StaticText(panel, -1, 'dc-v',(10,25)) 
        self.txt3 = wx.StaticText(panel, -1, 'bat-v',(10,40))

        bClear = wx.Button(panel, -1, "Run", pos=(5, 65))
        self.Bind(wx.EVT_BUTTON, self.OnClear, bClear)
        bQuit = wx.Button(panel, -1, "Quit", pos=(90, 65))
        self.Bind(wx.EVT_BUTTON, self.OnQuit, bQuit)
        
        MenuBar = wx.MenuBar()
        menu =wx.Menu()
        menu.Append(wx.ID_EXIT, 'E&xit\tAlt-X', 'exit')
        MenuBar.Append(menu,'&file')
#        self.picture=wx.StaticBitmap(panel)
        panel.SetBackgroundColour(wx.WHITE)
        
 #       self.picture.SetBitmap(wx,Bitmap('raspberry.bmp'))

        self.Centre() 
        self.Show(True) 

   def OnClear(self, event):
        uart.write("Run!!\r\n")
        pygame.mixer.music.load("ding-dong.wav")
        pygame.mixer.music.play()
       
   def OnQuit(self, event):
        uart.write("Quit!!\r\n")
        pygame.mixer.music.load('Alert.wav')
        pygame.mixer.music.play()
        self.Destroy()


class MyTimer(wx.Timer): 
    def Notify(self): 
        f.txt.SetLabel('Temprature :' + str(adc.read_temp(0))+' degC') 
        f.txt2.SetLabel('DC Voltage :' +str(adc.read_voltage(6))+' V') 
        f.txt3.SetLabel('BAT Voltage :' +str(adc.read_voltage(7))+' V') 
#        f.txt3.SetLabel(unicode(sh.Cells(3,1).Value)) 

app = wx.App(0) 
f = Application(None) 
t = MyTimer() 
t.Start(500) 
app.MainLoop()
