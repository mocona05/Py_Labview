from Tkinter import *
import time
import ads7828
import serial
import pygame
import wx

usbport ='/dev/ttyAMA0'
uart=serial.Serial(usbport,115200)
pygame.mixer.init()


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

app = wx.App(0) 
f = Application(None) 
t = MyTimer() 
t.Start(500) 
app.MainLoop()
