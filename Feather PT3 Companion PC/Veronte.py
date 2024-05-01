import time
import sys
import os
import serial

class Veronte:

    def __init__(self,Veronteport,Verontebitrate):
        self.Veronteport = Veronteport
        self.Verontebitrate = Verontebitrate
        self.Data = ''
        self.packet = [bytes('', 'ascii')]

        self.VeronteSerial =  serial.Serial(self.Veronteport,self.Verontebitrate,timeout = 1) # connect to the LoRa Modules 's serial port
        print("Init")
     
    def packetStruct(self):

        return self.packet

    def readData(self):
        while self.Dataleft > 0:
            self.Data = self.VeronteSerial.read()
            time.sleep(0.01)
            self.Dataleft = self.VeronteSerial.in_waiting()
            self.Data += self.VeronteSerial.read(self.Dataleft)
        return self.Data
