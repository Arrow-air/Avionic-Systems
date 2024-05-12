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
import serial
import threading
from multiprocessing import Process
import concurrent.futures

import can
import UI
import ESC
import BMS
import Veronte
import Joystick
import LoRa
import UDP
import Data

''' LINUX Systems
#arduino =  serial.Serial('/dev/ttyUSB0', 9600,timeout = 1) # connect to the arduino's serial port
#LoRaCPC =  serial.Serial('/dev/ttyUSB1', 115200,timeout = 1) # connect to the arduino's serial port
Lora = LoRaComms.LoRaComms('/dev/ttyUSB1',115200)
veronte = Veronte.Veronte('/dev/ttys0',115200)
time.sleep(2)
'''

''' Windows Systems
#arduino =  serial.Serial('COM4', 9600,timeout = 1)  # connect to the arduino's serial port
#LoRaCPC =  serial.Serial('COM10', 115200,timeout = 1) # connect to the Lora Module's serial port
'''
pygame.init()
pydisplay = pygame.display
pytime = pygame.time
pyjoystick = pygame.joystick
pyclock = pygame.time.Clock()

esc = ESC.ESC()
bms = BMS.BMS()
udp = UDP.UDP()

lora = LoRa.LoRa('COM10',115200)
veronte = Veronte.Veronte('COM9',115200)
ui = UI.UI(pydisplay,pytime,'GCS')
data = Data.Data(lora,udp,ui)

#joystick = Joystick.Joystick(pyjoystick,pytime)
joystickUSB = Joystick.JoystickUSB(pyjoystick,pytime)
joystickCAN = Joystick.JoystickCAN(pyjoystick,pytime)

time.sleep(5)

def dataUpdate():
    data.JoystickPacket = joystickUSB.packetStruct()
    #data.JoystickPacket = joystickCAN.packetStruct()
    print(data.JoystickPacket)
    data.ESCPacket = esc.packetStruct()
    data.BMSPacket  = bms.packetStruct()
    data.VerontePacket  = veronte.packetStruct()
    data.now = str(datetime.now())
    pass

EXIT = False

if __name__ == '__main__':
    while not EXIT:
        #data.JoystickPacket = joystickUSB.packetStruct()
        #data.JoystickPacket = joystickCAN.packetStruct()
        #print(data.JoystickPacket)

        #dataUpdate()

        dataThread = threading.Thread(target=dataUpdate)
        uiThread = threading.Thread(target=data.uiUpdate)
        logThread = threading.Thread(target=data.logUpdate)
        telematryThread = threading.Thread(target=data.telemetryUpdate)
        
        dataThread.start()
        uiThread.start()
        logThread.start()
        telematryThread.start()

        dataThread.join()
        uiThread.join()
        logThread.join()
        telematryThread.join()
        data.uiUpdate()

        #dataProcess = Process(target=dataUpdate)
        #uiProcess = Process(target=data.uiUpdate)
        #logThreaProcess = Process(target=data.logUpdate)
        #telematryProcess = Process(target=data.telemetryUpdate)

        #dataProcess.start()
        #uiProcess.start()
        #logThreaProcess.start()
        #telematryProcess.start()

        #dataProcess.join()
        #uiProcess.join()
        #logThreaProcess.join()
        #telematryProcess.join()

        #with concurrent.futures.ThreadPoolExecutor() as executor:
            #dataFuture = executor.submit(dataUpdate)
            #data.JoystickPacket = bytes(JoystickFuture.result(),'ascii')
            #data.JoystickPacket = JoystickCAN.packetStruct()

            #data.ESCPacket = esc.packetStruct()
            #print(data.ESCPacket)

            #data.BMSPacket  = bms.packetStruct()
            #print(data.BMSPacket)

            #data.VerontePacket  = veronte.packetStruct()
            #print(data.VerontePacket)

            #data.now = str(datetime.now())
            #print(data.now)

            #uiFuture = executor.submit(data.uiUpdate)
            #logFuture = executor.submit(data.logUpdate)
            #telematryFuture = executor.submit(data.telemetryUpdate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT = True

        if  str(data.JoystickPacket[4]) == "b'001'":
            pygame.quit()                           # This is used to quit pygame and use any internal program within the python
            quit()

        #pyclock.tick(1000)

    pygame.quit()
    quit()


