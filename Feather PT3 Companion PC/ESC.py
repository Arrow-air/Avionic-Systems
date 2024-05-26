import CyphalCAN
import asyncio

class ESC:

    def __init__(self,modeselect) -> None:

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        
        self.packet = {}
        self.Superpacket = {}

        self.dataDictionary = {'ESC1_temp_C':0, 'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,'ESC5_temp_C':0,'ESC6_temp_C':0,
                               'MOT1_temp_C':0,'MOT2_temp_C':0,'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':0,
                               'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':0,
                               'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':0,
                               'ESC1_CUR_AMP':0,'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0}

        self.esc1 = CyphalCAN(10)
        self.esc2 = CyphalCAN(11)
        self.esc3 = CyphalCAN(12)
        self.esc4 = CyphalCAN(13)
        self.esc5 = CyphalCAN(14)
        self.esc6 = CyphalCAN(15)

        print("ESC Init")

    def packetStruct(self):

        self.Superpacket = self.escRead()


        return self.packet
    
    def escRead(self):
        for x in range(1,6):
            asyncio.run("esc{x}".send_command(node_id=9+x, command=0x01))
            asyncio.run("esc{x}".read_register(node_id=9+x, register_index=0x04))
            asyncio.run("esc{x}".receive_data())
            data = "esc{x}".get_data()
            self.Superpacket = self.Superpacket | data 

        return self.Superpacket

