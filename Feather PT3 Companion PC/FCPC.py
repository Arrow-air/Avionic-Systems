#!/usr/bin/env python
'''
Arrow Air 2024

Project Feather Flight Companinon Computer

Data Logger
Telemetry Server
User Interface Engine

'''
import time
from datetime import datetime
import pygame
import threading
import socket

import can
import IO
import UI
import ESC
import BMS
import Veronte
import Joystick
import LoRa
import TCP
import Data

#gound_or_flight = 'GCS' #GroundControlStation
gound_or_flight = 'FUI' #Flight UI

'''
LoraComport = 'COM10'   #Lora Serial Port
VeronteComport = 'COM9' #Veronte Serial Port
Serialbitrate = 115200
'''


LoraComport = '/dev/tty9'   #Lora Serial Port
VeronteComport = '/dev/tty10' #Veronte Serial Port
Serialbitrate = 115200



''' LINUX Systems
Lora = LoRaComms.LoRaComms('/dev/ttyUSB1',115200)
veronte = Veronte.Veronte('/dev/ttys0',115200)
time.sleep(2)
'''

''' Windows Systems
Lora = LoRaComms.LoRaComms('COM10',115200
veronte = Veronte.Veronte('COM9',115200)
time.sleep(2)
'''

TCP_IP = socket.gethostname() #'192.168.1.84'# #"127.0.0.1"
print(TCP_IP)
TCP_PORT = 1234
TCP_Buffer = 16

pygame.init()
pydisplay = pygame.display
pytime = pygame.time
pyjoystick = pygame.joystick
pyclock = pygame.time.Clock()

if gound_or_flight == 'FUI':
    io = IO.IO(gound_or_flight)
    esc = ESC.ESC(gound_or_flight)
    bms = BMS.BMS(gound_or_flight)
    tcp = TCP.TCP(TCP_IP,TCP_PORT,TCP_Buffer,gound_or_flight)

    lora = LoRa.LoRa(LoraComport,Serialbitrate,gound_or_flight)
    veronte = Veronte.Veronte(VeronteComport,Serialbitrate,gound_or_flight)
    ui = UI.UI(pydisplay,pytime,gound_or_flight)
    data = Data.Data(lora,tcp,ui,gound_or_flight)

    joystickUSB = Joystick.JoystickUSB(pyjoystick,pytime,gound_or_flight)
    #joystickCAN = Joystick.JoystickCAN(pyjoystick,pytime,gound_or_flight)

elif gound_or_flight == 'GCS':
    tcp = TCP.TCP(TCP_IP,TCP_PORT,TCP_Buffer,gound_or_flight)
    lora = LoRa.LoRa(LoraComport,Serialbitrate,gound_or_flight)
    ui = UI.UI(pydisplay,pytime,gound_or_flight)
    data = Data.Data(lora,tcp,ui,gound_or_flight)

tlock = threading.Lock()

def dataUpdate():
    data.JoystickPacket = joystickUSB.packetStruct()
    #data.JoystickPacket = joystickCAN.packetStruct()
    data.IOPacket = io.packetStruct()
    data.ESCPacket = esc.packetStruct()
    data.BMSPacket  = bms.packetStruct()
    data.VerontePacket  = veronte.packetStruct()
    data.now['TimeStamp'] = str(datetime.now())
    data.packetStruct()

EXIT = False

if __name__ == '__main__':
    
    while not EXIT:

        if gound_or_flight == 'FUI':

            dataThread = threading.Thread(target=dataUpdate)
            logThread = threading.Thread(target=data.logUpdate)
            telematryThread = threading.Thread(target=data.telemetryUpdate,daemon=True)
            
            dataThread.start()
            logThread.start()
            telematryThread.start()

            dataThread.join()
           
            data.uiUpdate()

        elif gound_or_flight == 'GCS':

            gcsThread = threading.Thread(target=data.gcsUpdate,daemon=True)

            gcsThread.start()

            data.uiUpdate()

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


