from datetime import datetime
import os
import threading

class Data:

    def __init__(self,TCP,modeselect) -> None:
        
        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        #self.Lora = Lora
        #self.Lora.LoRaconfig()
        
        self.TCP = TCP

        self.packet = {}
        self.dataString = ''
        
        self.tlock = threading.Lock()

        self.now = {'TimeStamp':0}

        self.JoystickPacket  = {'command_pitch':0.2,'command_roll':0,'command_yaw':0,'command_throttle':0.3,'switch_states':0}

        self.ParachutePacket = {'parachute_state':0}

        self.VerontePacket  = {'altitude_AGL':0,'altitude_AGL_set':0,'altitude_ABS':0,'altitude_AGL':0,'heading':0,'compass':0,'attitude_pitch':0,'attitude_roll':0,'vertical_speed_KTS':0,
                               'airspeed_KTS':0,'OAT':0,'altitude_ABS':40,'latitude':'40d26a46q','longitude':'79d58a56q','flight_time':'50:39'}
        
        self.BMSPacket  = {'BAT1_temp_C':0,'BAT2_temp_C':30,'BAT3_temp_C':0,'BAT4_temp_C':0,'BAT5_temp_C':0,'BAT6_temp_C':0,'ESC1_temp_C':0,
                               'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,'ESC5_temp_C':0,'ESC6_temp_C':0,'MOT1_temp_C':0,'MOT2_temp_C':0,
                               'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':60,'MOT6_temp_C':0,'BAT1_soc_PCT':0,'BAT2_soc_PCT':0,'BAT3_soc_PCT':0,
                               'BAT4_soc_PCT':0,'BAT5_soc_PCT':0,'BAT6_soc_PCT':0,'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,
                               'MOT5_rpm_PCT':100,'MOT6_rpm_PCT':50,'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':100,'ESC1_CUR_AMP':0,
                               'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0}
        
        self.ESCPacket = {'ESC1_temp_Ce':0, 'ESC2_temp_Ce':0,'ESC3_temp_Ce':0,'ESC4_temp_Ce':0,'ESC5_temp_Ce':0,'ESC6_temp_Ce':0,
                          'MOT1_temp_Ce':0,'MOT2_temp_Ce':0,'MOT3_temp_Ce':0,'MOT4_temp_Ce':0,'MOT5_temp_Ce':0,'MOT6_temp_Ce':0,
                          'MOT1_rpm_PCTe':0,'MOT2_rpm_PCTe':0,'MOT3_rpm_PCTe':0,'MOT4_rpm_PCTe':0,'MOT5_rpm_PCTe':0,'MOT6_rpm_PCTe':0,
                          'ESC1_Ve':0,'ESC2_Ve':0,'ESC3_Ve':0,'ESC4_Ve':0,'ESC5_Ve':0,'ESC6_Ve':0,
                          'ESC1_CUR_AMPe':0,'ESC2_CUR_AMPe':0,'ESC3_CUR_AMPe':0,'ESC4_CUR_AMPe':0,'ESC5_CUR_AMPe':0,'ESC6_CUR_AMPe':0}
        
        self.IOPacket = {}

        self.dataDictionary = {}

        
        self.parameters = {
            "altitude_AGL":0,
            "altitude_AGL_set":0,
            "altitude_ABS":0,
            "heading":0,
            "compass":0,
            "attitude_pitch":0, # forward-backward rotation of the aircraft itself, in what angle the aircraft is leaning to forward or backward, range: -180 to 180(minus is leaning backward, positive is leaning forward)
            "attitude_roll":0, # right-left rotation of the aircraft itself, in what angle the aircraft is leaning side wise, range: -180 to 180(minus is leaning to the left side, positive is to the right side)
            "vertical_speed_KTS":0,
            "airspeed_KTS":0, # warning range: 55-60,-60-(-55), [kts], speed will be between 0-60 knots
            "OAT":0, # warning range: 30-max=100
            "latitude":'40d26a46q',
            'longitude':'79d58a56q',
            "flight_time":'59:39',

            "command_pitch":0, # right joystick, up-down, range: -1 to 1
            "command_roll":0, # right joystick, left-right, range: -1 to 1
            "command_throttle":0, # left joystick, up-down, range: -1 to 1
            "command_yaw":0, # left joystick, left-right, range: -1 to 1
            "switch_states":0,

            "parachute_state":0,

            "BAT1_temp_C":0, # warning range: 80-180
            "BAT2_temp_C":0, # warning range: 80-180
            "BAT3_temp_C":0, # warning range: 80-180
            "BAT4_temp_C":0, # warning range: 80-180
            "BAT5_temp_C":0, # warning range: 80-180
            "BAT6_temp_C":0, # warning range: 80-180

            "ESC1_temp_C":0,
            "ESC2_temp_C":0,
            "ESC3_temp_C":0,
            "ESC4_temp_C":0,
            "ESC5_temp_C":0,
            "ESC6_temp_C":0,

            "MOT1_temp_C":0,
            "MOT2_temp_C":0,
            "MOT3_temp_C":0,
            "MOT4_temp_C":0,
            "MOT5_temp_C":0,
            "MOT6_temp_C":0,

            "BAT1_soc_PCT":90, # the percentage of the battery left, warning range: 1-15
            "BAT2_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
            "BAT3_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
            "BAT4_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
            "BAT5_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
            "BAT6_soc_PCT":100, # the percentage of the battery left, warning range: 1-15

            "MOT1_rpm_PCT":0, # warning range: 120-max=140
            "MOT2_rpm_PCT":0, # warning range: 120-max=140
            "MOT3_rpm_PCT":0, # warning range: 120-max=140
            "MOT4_rpm_PCT":0, # warning range: 120-max=140
            "MOT5_rpm_PCT":0, # warning range: 120-max=140
            "MOT6_rpm_PCT":0, # warning range: 120-max=140

            "ESC1_V":0,
            "ESC2_V":0,
            "ESC3_V":0,
            "ESC4_V":0,
            "ESC5_V":0,
            "ESC6_V":0,
            
            "ESC1_CUR_AMP":0,
            "ESC2_CUR_AMP":0,
            "ESC3_CUR_AMP":0,
            "ESC4_CUR_AMP":0,
            "ESC5_CUR_AMP":0,
            "ESC6_CUR_AMP":0,
            "TimeStamp":0
        }

        try:
            os.mkdir('./Logs')
        except OSError as error:
            pass

        self.Starttimestamp = str(datetime.now().year)+ '_' + str(datetime.now().month)+ '_' + str(datetime.now().day) + '-' + str(datetime.now().hour) + '_' + str(datetime.now().minute)
        self.logFile = open('./Logs/FeatherFlightLog-'+self.Starttimestamp+'.csv','w',encoding='utf-8')
        
        print("Data Init")

    def packetStruct(self):
        self.V = self.VerontePacket.keys()
        self.J = self.JoystickPacket.keys()
        self.B = self.BMSPacket.keys()
        self.E = self.ESCPacket.keys()

        for key in self.V:
            self.parameters[key] = self.VerontePacket[key]
        for key in self.J:
            self.parameters[key] = self.JoystickPacket[key]
        for key in self.B:
            self.parameters[key] = self.BMSPacket[key]
        
        self.ParachutePacket['parachute_state'] = 0
        self.parameters['TimeStamp'] = self.now['TimeStamp']
        self.packet = str(self.parameters)

    def logUpdate(self):
        self.logPacket = self.VerontePacket | self.JoystickPacket | self.ParachutePacket | self.BMSPacket | self.ESCPacket | self.IOPacket | self.now
        #print(self.logPacket)
        self.logFile.write(str(self.logPacket) + '\n')
        
        return 0

    def telemetryUpdate(self):
        self.telemetryPacket = self.packet
        with self.tlock:
            #self.Lora.packet = bytes(str(self.telemetryPacket) + '\n', 'ascii')
            #self.Lora.LoRaTransmit()
            self.TCP.packet = self.telemetryPacket + '\n'
            self.TCP.TCPServer()
        return 0
    
    def gcsUpdate(self):
        self. dataString = self.TCP.TCPClient()
        self.packet = self.dataString
        #print(self.dataString)
        #selfdataDictionary = ast.literal_eval(self. dataString)
