#!/usr/bin/env python
'''
Arrow Air 2024

Project Feather Flight Companinon Computer

Data Logger
Telemetry Server
User Interface Engine

'''
import os
import sys
import time
import pygame
import serial
import threading

import UI
import ESC
import BMS
import Veronte
import Joystick
import LoRa
import Data

''' LINUX Systems
#arduino =  serial.Serial('/dev/ttyUSB0', 9600,timeout = 1) # connect to the arduino's serial port
#LoRaCPC =  serial.Serial('/dev/ttyUSB1', 115200,timeout = 1) # connect to the arduino's serial port
Lora = LoRaComms.LoRaComms('/dev/ttyUSB1',115200)
veronte = Veronte.Veronte('/dev/ttys0',115200)
time.sleep(2)
'''

'''Windows Systems'''
#arduino =  serial.Serial('COM4', 9600,timeout = 1)  # connect to the arduino's serial port
#LoRaCPC =  serial.Serial('COM10', 115200,timeout = 1) # connect to the Lora Module's serial port

pygame.init()
ui = UI.UI()
esc = ESC.ESC()
bms = BMS.BMS()
lora = LoRa.LoRa('COM10',115200)
JoystickUSB = Joystick.JoystickUSB()
JoystickCAN = Joystick.JoystickCAN()
veronte = Veronte.Veronte('COM9',115200)
data = Data.Data(lora,ui)
time.sleep(5)

clock = pygame.time.Clock()                 # intialise pygame refresh and call it clock

EXIT = False
    
while not EXIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXIT = True

    data.JoystickPacket = JoystickUSB.packetStruct()
    #data.JoystickPacket = JoystickCAN.packetStruct()
    #print(data.JoystickPacket)

    data.ESCPacket = esc.packetStruct()
    #print(data.ESCPacket)

    data.BMSPacket  = bms.packetStruct()
    #print(data.BMSPacket)

    data.VerontePacket  = veronte.packetStruct()
    #print(data.VerontePacket)

    data.uiUpdate()
    data.logUpdate()
    data.telemetryUpdate()

    if  str(data.JoystickPacket[4]) == "b'001'":
        pygame.quit()                           # This is used to quit pygame and use any internal program within the python
        quit()

    clock.tick(1000)

pygame.quit()
quit()
