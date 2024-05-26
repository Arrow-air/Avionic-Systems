import time
import serial
import random

class Veronte:

    def __init__(self,Veronteport,Verontebitrate,modeselect):

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        self.Veronteport = Veronteport
        self.Verontebitrate = Verontebitrate
        
        self.VeronteSerial =  serial.Serial(self.Veronteport,self.Verontebitrate,timeout = 1) # connect to the LoRa Modules 's serial port
        
        self.Data = ''
        self.packet = {}
        self.dataDictionary = {'altitude_AGL':0,'altitude_AGL_set':0,'altitude_ABS':0,'altitude_AGL':0,'heading':0,'compass':0,'attitude_pitch':0,'attitude_roll':0,'vertical_speed_KTS':0,
                               'airspeed_KTS':0,'OAT':0,'altitude_ABS':0}

        print("Veronte Init")
        
    def packetStruct(self):
        
        #self.data = self.readData()
        #self.dataDictionary = ast.literal_eval(self.data)
        #self.packet = self.dataDictionary
        
        self.packet = {'altitude_AGL':random.uniform(0,100),'altitude_AGL_set':random.uniform(0,100),'altitude_ABS':random.uniform(0,100),'altitude_AGL':random.uniform(0,100),'heading':random.uniform(0,360),'compass':random.uniform(0,360),'attitude_pitch':random.uniform(-30,30),'attitude_roll':random.uniform(-30,30),'vertical_speed_KTS':random.uniform(0,60),
                       'airspeed_KTS':random.uniform(0,60),'OAT':random.uniform(0,100),"latitude":'40d26a46q','longitude':'79d58a56q',"flight_time":(str(random.randint(0,59))+':'+str(random.randint(0,59)))}
        
        #print(self.packet)
        return self.packet

    def readData(self):
        
        self.Dataleft = self.VeronteSerial.inWaiting()
        
        while self.Dataleft > 0:
            
            self.Data = self.VeronteSerial.read()
            time.sleep(0.01)
            self.Dataleft = self.VeronteSerial.inWaiting()
            self.Data += self.VeronteSerial.read(self.Dataleft)
            
        return self.Data
