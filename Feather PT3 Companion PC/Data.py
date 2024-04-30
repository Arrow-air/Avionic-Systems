import time
import sys
import os

class Data:

    def __init__(self) -> None:
        self.ESCPacket = []
        self.BMSPacket  = []
        self.VerontePacket  = []
        self.JoystickPacket  = []
        self.ParachutePacket  = []

    def packetStruct(self):
        return 0

    def uiUpdate(self):
        return 0

    def telemetryUpdate(self):
        return 0

    def logUpdate(self):
        return 0

