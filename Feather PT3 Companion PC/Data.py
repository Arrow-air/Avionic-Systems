from datetime import datetime
import os
import threading
import ast

class Data:

    def __init__(self,Lora,TCP,UI,modeselect) -> None:
        
        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        self.Lora = Lora
        self.TCP = TCP
        self.UI = UI

        self.packet = ''
        self.dataString = ''

        self.now = {'TimeStamp':''}

        self.JoystickPacket  = {'command_pitch':0,'command_roll':0,'command_yaw':0,'command_throttle':0,'switch_states':0}

        self.VerontePacket  = {'altitude_AGL':0,'altitude_AGL_set':0,'altitude_ABS':0,'altitude_AGL':0,'heading':0,'compass':0,'attitude_pitch':0,'attitude_roll':0,'vertical_speed_KTS':0,
                               'airspeed_KTS':0,'OAT':0,'altitude_ABS':0}
        
        self.BMSPacket  = {'BAT1_temp_C':0,'BAT2_temp_C':0,'BAT3_temp_C':0,'BAT4_temp_C':0,'BAT5_temp_C':0,'BAT6_temp_C':0,'ESC1_temp_C':0,
                               'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,'ESC5_temp_C':0,'ESC6_temp_C':0,'MOT1_temp_C':0,'MOT2_temp_C':0,
                               'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':0,'BAT1_soc_PCT':0,'BAT2_soc_PCT':0,'BAT3_soc_PCT':0,
                               'BAT4_soc_PCT':0,'BAT5_soc_PCT':0,'BAT6_soc_PCT':0,'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,
                               'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':0,'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':0,'ESC1_CUR_AMP':0,
                               'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0}
        
        self.ParachutePacket = {'parachute_state':0}
        
        self.IOPacket = []
        self.ESCPacket = []

        self.dataDictionary = ''

        '''
        self.dataDictionary = {'altitude_AGL':0,'altitude_AGL_set':0,'altitude_ABS':0,'altitude_AGL':0,'heading':0,'compass':0,'attitude_pitch':0,'attitude_roll':0,'vertical_speed_KTS':0,
                               'airspeed_KTS':0,'OAT':0,'altitude_ABS':0,'command_pitch':0,'command_roll':0,'command_yaw':0,'switch_states':0,'parachute_state':0,'BAT1_temp_C':0,
                               'BAT2_temp_C':0,'BAT3_temp_C':0,'BAT4_temp_C':0,'BAT5_temp_C':0,'BAT6_temp_C':0,'ESC1_temp_C':0,'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,
                               'ESC5_temp_C':0,'ESC6_temp_C':0,'MOT1_temp_C':0,'MOT2_temp_C':0,'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':0,'BAT1_soc_PCT':0,
                               'BAT2_soc_PCT':0,'BAT3_soc_PCT':0,'BAT4_soc_PCT':0,'BAT5_soc_PCT':0,'BAT6_soc_PCT':0,'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,
                               'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':0,'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':0,'ESC1_CUR_AMP':0,
                               'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0,'TimeStamp':0}
        '''

        self.tlock = threading.Lock()

        self.Lora.LoRaconfig()


        try:
            os.mkdir('./Logs')
        except OSError as error:
            pass

        self.Starttimestamp = str(datetime.now().year)+ '_' + str(datetime.now().month)+ '_' + str(datetime.now().day) + '-' + str(datetime.now().hour) + '_' + str(datetime.now().minute)
        self.logFile = open('./Logs/FeatherFlightLog-'+self.Starttimestamp+'.csv','w',encoding='utf-8')
        print("Data Init")

    def packetStruct(self):

        self.packet = str(self.JoystickPacket | self.VerontePacket | self.ParachutePacket | self.BMSPacket | self.now )

    def uiUpdate(self):
        self.uiPacket = self.packet
        self.UI.uiUpdate(self.uiPacket)
        return 0
    
    def logUpdate(self):
        self.logPacket = self.packet
        print(self.logPacket)
        self.logFile.write(str(self.logPacket) + '\n')
        
        return 0

    def telemetryUpdate(self):
        self.telemetryPacket = self.packet
        with self.tlock:
            self.Lora.packet = bytes(str(self.telemetryPacket) + '\n', 'ascii')
            self.Lora.LoRaTransmit()
            self.TCP.packet = str(self.telemetryPacket) + '\n'
            self.TCP.TCPServer()
        return 0
    
    def gcsUpdate(self):
        self. dataString = self.TCP.TCPClient()
        self.packet = self.dataString
        #print(self.dataString)
        #selfdataDictionary = ast.literal_eval(self. dataString)