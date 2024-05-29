import VESCCAN

class BMS:

    def __init__(self,modeselect) -> None:
        
        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        
        self.vesc = VESCCAN.VESCCAN()

        self.packet = {}
        self.rawData = {}

        '''
        self.dataDictionary = {'BAT1_temp_C':0,'BAT2_temp_C':0,'BAT3_temp_C':0,'BAT4_temp_C':0,'BAT5_temp_C':0,'BAT6_temp_C':0,'ESC1_temp_C':0,
                               'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,'ESC5_temp_C':0,'ESC6_temp_C':0,'MOT1_temp_C':0,'MOT2_temp_C':0,
                               'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':0,'BAT1_soc_PCT':0,'BAT2_soc_PCT':0,'BAT3_soc_PCT':0,
                               'BAT4_soc_PCT':0,'BAT5_soc_PCT':0,'BAT6_soc_PCT':0,'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,
                               'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':0,'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':0,'ESC1_CUR_AMP':0,
                               'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0}
        '''
        
        self.dataDictionary = {'BAT1_temp_C':0,'BAT2_temp_C':0,'BAT3_temp_C':0,'BAT4_temp_C':0,'BAT5_temp_C':0,'BAT6_temp_C':0,
                               'ESC1_temp_C':0,'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,'ESC5_temp_C':0,'ESC6_temp_C':0,
                               'MOT1_temp_C':0,'MOT2_temp_C':0,'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':0,
                               'BAT1_soc_PCT':0,'BAT2_soc_PCT':0,'BAT3_soc_PCT':0,'BAT4_soc_PCT':0,'BAT5_soc_PCT':0,'BAT6_soc_PCT':0,
                               'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':0,
                               'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':0,
                               'ESC1_CUR_AMP':0,'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0}
        
        print("BMS Init")

    def packetStruct(self):

        self.packet = self.bmsRead()
        
        for x in range(10,15):
           
           if self.packet['unit_id'] == x:
               
               y = x - 9
               self.dataDictionary[f'BAT{y}_temp_C'] = self.packet['CAN_PACKET_BMS_TEMP0']
               self.dataDictionary[f'BAT{y}_soc_PCT'] = self.packet['SOC']
               self.dataDictionary[f'ESC{y}_V'] = self.packet['packVoltage']
               self.dataDictionary[f'ESC{y}_CUR_AMP'] = self.packet['packCurrent1']

        self.packet = self.dataDictionary
    
        '''
        self.packet = {'BAT1_temp_C':random.randint(0,100),'BAT2_temp_C':random.randint(0,100),'BAT3_temp_C':random.randint(0,100),'BAT4_temp_C':random.randint(0,100),'BAT5_temp_C':random.randint(0,100),'BAT6_temp_C':random.randint(0,100),'ESC1_temp_C':random.randint(0,100),
                               'ESC2_temp_C':0,'ESC3_temp_C':random.randint(0,100),'ESC4_temp_C':0,'ESC5_temp_C':0,'ESC6_temp_C':0,'MOT1_temp_C':0,'MOT2_temp_C':0,
                               'MOT3_temp_C':random.randint(0,100),'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':random.randint(0,100),'BAT1_soc_PCT':random.randint(0,100),'BAT2_soc_PCT':random.randint(0,100),'BAT3_soc_PCT':random.randint(0,100),
                               'BAT4_soc_PCT':random.randint(0,100),'BAT5_soc_PCT':0,'BAT6_soc_PCT':random.randint(0,100),'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,
                               'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':random.randint(0,100),'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':random.randint(0,100),'ESC1_CUR_AMP':0,
                               'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':random.randint(0,100),'ESC6_CUR_AMP':0}
        '''        
        print(self.packet) 
        return self.packet
    
    def bmsRead(self):

        self.rawData = self.vesc.read_frame()

        if self.rawData:

            print(self.rawData)

            return self.rawData