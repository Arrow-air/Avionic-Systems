import time
import sys
import os
import serial

class Veronte:

    def __init__(self,Veronteport,Verontebitrate,modeselect):

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        self.Veronteport = Veronteport
        self.Verontebitrate = Verontebitrate
        self.Data = ''
        self.dataDictionary = {'altitude_AGL':0,'altitude_AGL_set':0,'altitude_ABS':0,'altitude_AGL':0,'heading':0,'compass':0,'attitude_pitch':0,'attitude_roll':0,'vertical_speed_KTS':0,
                               'airspeed_KTS':0,'OAT':0,'altitude_ABS':0}
        self.packet = ['']

        self.VeronteSerial =  serial.Serial(self.Veronteport,self.Verontebitrate,timeout = 1) # connect to the LoRa Modules 's serial port
        print("Veronte Init")

    def packetStruct(self):
        self.packet = self.dataDictionary
        return self.packet

    def readData(self):
        while self.Dataleft > 0:
            self.Data = self.VeronteSerial.read()
            time.sleep(0.01)
            self.Dataleft = self.VeronteSerial.in_waiting()
            self.Data += self.VeronteSerial.read(self.Dataleft)
        return self.Data
