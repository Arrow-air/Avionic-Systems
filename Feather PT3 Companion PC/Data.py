import time
from datetime import datetime
import sys
import os

class Data:

    def __init__(self,Lora,UI) -> None:
        self.Lora = Lora
        self.ui = UI

        self.ESCPacket = []
        self.BMSPacket  = []
        self.VerontePacket  = []
        self.JoystickPacket  = []
        self.ParachutePacket  = []

        self.uiPacket = []
        self.logPacket = []
        self.telemetryPacket = []

        self.Lora.LoRaconfig()

        try:
            os.mkdir('./Logs')
        except OSError as error:
            print(error)

        self.Starttimestamp = str(datetime.now().year)+ '_' + str(datetime.now().month)+ '_' + str(datetime.now().day) + '-' + str(datetime.now().hour) + '_' + str(datetime.now().minute)
        self.logFile = open('./Logs/FeatherFlightLog-'+self.Starttimestamp+'.csv','w',encoding='utf-8')

    def packetStruct(self):
        return 0

    def uiUpdate(self):
        self.uiPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        return 0
    
    def logUpdate(self):
        self.logPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket
        self.logFile.write(str(self.logPacket)+ '-' + str(datetime.now()) + '\n')
        return 0

    def telemetryUpdate(self):
        self.telemetryPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        self.Lora.packet = bytes(str(self.telemetryPacket)+ '-' + str(datetime.now()) +'\n', 'ascii')
        self.Lora.LoRaTransmit()
        return 0