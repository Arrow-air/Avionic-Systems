#!/usr/bin/env python

'''

Arrow Air 2024

Project Feather Flight Companinon Computer

Ground Control Station & Onboard Flight UI

Functions:
1) Data Logger
2) Telemetry Server
3) User Interface Engine

'''

#Python Built-in Packages
import time
import pygame
import socket
from datetime import datetime

#Created Packages 
import IO
import UI
import ESC
import BMS
import LoRa
import TCP
import Data
import Veronte
import Joystick

#Onboard Flight UI or Ground Control Station Selector
#gound_or_flight = 'GCS' #GroundControlStation
gound_or_flight = 'FUI' #Flight UI

#Serial Comport Settings for Lora Telemetry & Flight Controller Interfaces
''' TEST
LoraComport = 'COM10'   #Lora Serial Port
VeronteComport = 'COM9' #Veronte Serial Port
Serialbitrate = 115200
'''

#LoraComport = '/dev/tty6'   #Lora Serial Port
VeronteComport = '/dev/ttyS0' #Veronte Serial Port
Serialbitrate = 115200

#IP seting for TCP/IP Telemetry
TCP_IP = socket.gethostname() #'192.168.1.84'# #"127.0.0.1"
TCP_PORT = 1234
TCP_Buffer = 16

#Pygame Intitialisation for joysticks
pygame.init()
pydisplay = pygame.display
pytime = pygame.time
pyjoystick = pygame.joystick
pyclock = pygame.time.Clock()

#Module Initialisation for onboard Flight UI
if gound_or_flight == 'FUI':
    io = IO.IO(gound_or_flight)
    esc = ESC.ESC(gound_or_flight)
    bms = BMS.BMS(gound_or_flight)
    tcp = TCP.TCP(TCP_IP,TCP_PORT,TCP_Buffer,gound_or_flight)

    #lora = LoRa.LoRa(LoraComport,Serialbitrate,gound_or_flight)
    veronte = Veronte.Veronte(VeronteComport,Serialbitrate,gound_or_flight)
    #ui = UI.UI(pydisplay,pytime,gound_or_flight)
    data = Data.Data(tcp,gound_or_flight)

    joystickUSB = Joystick.JoystickUSB(pyjoystick,pytime,gound_or_flight)
    #joystickCAN = Joystick.JoystickCAN(pyjoystick,pytime,gound_or_flight)

#Module Initialisation for GroundControl UI
elif gound_or_flight == 'GCS':
    tcp = TCP.TCP(TCP_IP,TCP_PORT,TCP_Buffer,gound_or_flight)
    #lora = LoRa.LoRa(LoraComport,Serialbitrate,gound_or_flight)
    #ui = UI.UI(pydisplay,pytime,gound_or_flight)
    data = Data.Data(tcp,gound_or_flight)

tlock = threading.Lock()

EXIT = False

if __name__ == '__main__':
    
    while not EXIT:

        if gound_or_flight == 'FUI':
            
            #Return Data From Each System Module
            data.JoystickPacket = joystickUSB.packetStruct()
            #data.JoystickPacket = joystickCAN.packetStruct()
            #data.IOPacket = io.packetStruct()
            #data.ESCPacket = esc.packetStruct()
            data.VerontePacket  = veronte.packetStruct()
            data.BMSPacket  = bms.packetStruct()
            data.now['TimeStamp'] = str(datetime.now())
            data.packetStruct()
            
            #Wrtie Data log file
            #data.logUpdate()
            
            #Send Data to GCS
            data.telemetryUpdate()

        elif gound_or_flight == 'GCS':
            
            #Read Data from Telemtry and send to UI programs
            data.gscUpdate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lora.LoraTerminate()
                tcp.TCPTerminate()
                pygame.quit()
                EXIT = True

        if  str(data.JoystickPacket['switch_states']) == '001000' or str(data.JoystickPacket['switch_states']) == '001026' or str(data.JoystickPacket['switch_states']) == '000001':
            lora.LoraTerminate()
            tcp.TCPTerminate()
            pygame.quit()
            quit()

    pygame.quit()
    quit()


