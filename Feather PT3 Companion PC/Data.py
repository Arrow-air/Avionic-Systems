from datetime import datetime
import os

class Data:

    def __init__(self,Lora,UDP,UI) -> None:
        self.Lora = Lora
        self.UDP = UDP
        self.ui = UI

        self.now = ''
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
            pass

        self.Starttimestamp = str(datetime.now().year)+ '_' + str(datetime.now().month)+ '_' + str(datetime.now().day) + '-' + str(datetime.now().hour) + '_' + str(datetime.now().minute)
        #self.logFile = open('./Logs/FeatherFlightLog-'+self.Starttimestamp+'.csv','w',encoding='utf-8')

    def packetStruct(self):
        return 0

    def uiUpdate(self):
        self.uiPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        self.ui.background()
        self.ui.stateUpdate(self.uiPacket)
        self.ui.infoUpdate(self.uiPacket)
        self.ui.run(self.uiPacket)

        print(self.uiPacket)
        return 0
    
    def logUpdate(self):
        self.logPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket
        #print(self.logPacket)
        #self.logFile.write(str(self.logPacket) + ',' + '-' +  self.now  + '\n')
        return 0

    def telemetryUpdate(self):
        self.telemetryPacket = self.JoystickPacket + self.VerontePacket + self.BMSPacket + self.ESCPacket + self.ParachutePacket

        self.Lora.packet = bytes(str(self.telemetryPacket) + ',' + '-' + self.now +'\n', 'ascii')
        self.Lora.LoRaTransmit()
        self.UDP.UDPTransmit()
        return 0