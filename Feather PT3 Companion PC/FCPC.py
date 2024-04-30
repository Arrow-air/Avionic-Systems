#!/usr/bin/env python

import os
import sys
import time
import pygame
import serial
import threading

import LoRaComms
import Joystick
import Data

''' LINUX Systems
pygame.init()
#arduino =  serial.Serial('/dev/ttyUSB0', 9600,timeout = 1) # connect to the arduino's serial port
#LoRaCPC =  serial.Serial('/dev/ttyUSB1', 115200,timeout = 1) # connect to the arduino's serial port
Lora = LoRaComms.LoRaComms('/dev/ttyUSB1',115200)
Joystick = Joystick.Joystick()
time.sleep(2)
'''

'''Windows Systems'''
#arduino =  serial.Serial('COM4', 9600,timeout = 1)  # connect to the arduino's serial port
#LoRaCPC =  serial.Serial('COM10', 115200,timeout = 1) # connect to the Lora Module's serial port

pygame.init()
Lora = LoRaComms.LoRaComms('COM10',115200)
Joystick = Joystick.Joystick()
Data = Data.Data()
time.sleep(2)

Lora.LoRaconfig()

time.sleep(2)

clock = pygame.time.Clock()                 # intialise pygame refresh and call it clock

EXIT = False
    
while not EXIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXIT = True
        
    controls = Joystick.DOF4ControlUSB()
    buttons = Joystick.buttonsUSB()
    
    control = ['<' + controls[1],controls[3],controls[2],controls[0],buttons[0],buttons[1] + '>'+'\n'+'\r']         # save strings in a list
    cstring = ",".join(control)                 # convert list to a single string with commas seperating values
                
    print(cstring)
    #arduino.write(bytes(cstring, 'ascii'))                      # print string to shell and write data to arduino with a 0.1ms delay
    Lora.packet = bytes(cstring, 'ascii')
    Lora.LoRaTransmit()                      # print string to shell and write data to arduino with a 0.1ms delay
    time.sleep(0.2)
    
    if  Joystick.USBcontrols[1].get_button(1) == 1:
        pygame.quit()                           # This is used to quit pygame and use any internal program within the python
        quit()

    clock.tick(1000)

pygame.quit()
quit()
