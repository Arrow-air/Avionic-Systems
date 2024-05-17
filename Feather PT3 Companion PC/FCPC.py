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

#gound_or_flight = 'GCS' #GroundControlStation
gound_or_flight = 'FUI' #Flight UI

LoraComport = 'COM10'   #Lora Serial Port
VeronteComport = 'COM9' #Veronte Serial Port
Serialbitrate = 115200

TCP_IP = socket.gethostname() #"127.0.0.1"
print(TCP_IP)
TCP_PORT = 1234
TCP_Buffer = 50

pygame.init()
pydisplay = pygame.display
pytime = pygame.time
pyjoystick = pygame.joystick
pyclock = pygame.time.Clock()

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
            uiThread = threading.Thread(target=data.uiUpdate)
            logThread = threading.Thread(target=data.logUpdate)
            telematryThread = threading.Thread(target=data.telemetryUpdate,daemon=True)
            
            dataThread.start()
            uiThread.start()
            logThread.start()
            telematryThread.start()

            dataThread.join()
            uiThread.join() 
            #logThread.join()
            #telematryThread.join()

        elif gound_or_flight == 'GCS':

            gcsThread = threading.Thread(target=data.gcsUpdate,daemon=True)
            uiThread = threading.Thread(target=data.uiUpdate)

            gcsThread.start()
            uiThread.start()
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


