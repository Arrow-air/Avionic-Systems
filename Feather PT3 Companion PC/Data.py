import time
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

    def packetStruct(self):
        return 0

    def uiUpdate(self):
        self.uiPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        return 0
    
    def logUpdate(self):
        self.logPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        return 0

    def telemetryUpdate(self):
        self.telemetryPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        self.Lora.packet = bytes(str(self.telemetryPacket)+'\n', 'ascii')
        self.Lora.LoRaTransmit()
        return 0