import CyphalCAN
import asyncio

class ESC:

    def __init__(self,modeselect) -> None:

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        
        self.packet = {}
        self.superDictionary = []

        self.superpacket = {'command_control':{'command': '', 'node_id': 0}, 'throttle_data':0,'info_upload_6160':{'electrical_speed': 0,'bus_current': 0,'running_status': 0},
                           'info_upload_6161': {'output_throttle': 0,'bus_voltage': 0,'temperatures': 0},'heartbeat': {'power_on_time': 0,'health_status': 0,'current_mode': 0}}

        self.dataDictionary = {'ESC1_temp_Ce':0, 'ESC2_temp_Ce':0,'ESC3_temp_Ce':0,'ESC4_temp_Ce':0,'ESC5_temp_Ce':0,'ESC6_temp_Ce':0,
                               'MOT1_temp_Ce':0,'MOT2_temp_Ce':0,'MOT3_temp_Ce':0,'MOT4_temp_Ce':0,'MOT5_temp_Ce':0,'MOT6_temp_Ce':0,
                               'MOT1_rpm_PCTe':0,'MOT2_rpm_PCTe':0,'MOT3_rpm_PCTe':0,'MOT4_rpm_PCTe':0,'MOT5_rpm_PCTe':0,'MOT6_rpm_PCTe':0,
                               'ESC1_Ve':0,'ESC2_Ve':0,'ESC3_Ve':0,'ESC4_Ve':0,'ESC5_Ve':0,'ESC6_Ve':0,
                               'ESC1_CUR_AMPe':0,'ESC2_CUR_AMPe':0,'ESC3_CUR_AMPe':0,'ESC4_CUR_AMPe':0,'ESC5_CUR_AMPe':0,'ESC6_CUR_AMPe':0}
        self.escCount = 0
        self.esc = []

        for self.escCount in range(1,6):
            try:
                self.esc.append(CyphalCAN(9 + self.escCount))
            except:
                return self.escCount
            
            #self.esc2 = CyphalCAN(11)
            #self.esc3 = CyphalCAN(12)
            #self.esc4 = CyphalCAN(13)
            #self.esc5 = CyphalCAN(14)
            #self.esc6 = CyphalCAN(15)

        print("ESC Init")

    def packetStruct(self):

        asyncio.run(self.escRead())

        for i in range(0,5):

            data = self.superDictionary[0]

            x = i + 1
            
            self.dataDictionary[f'MOT{x}_rpm_PCTe'] = data['info_upload_6160']['electrical_speed']
            self.dataDictionary[f'ESC{x}_CUR_AMPe'] = data['info_upload_6160']['bus_current']
            self.dataDictionary[f'ESC{x}_Ve'] = data['info_upload_6161']['bus_voltage']
            self.dataDictionary[f'ESC{x}_temp_Ce'] = data['info_upload_6161']['temperatures']

        self.packet = self.dataDictionary

        return self.packet
    
    '''
    def escRead(self):

        for x in range(1,6):
            
            asyncio.run(f'esc{x}'.send_command(node_id=9+x, command=0x01))
            asyncio.run(f'esc{x}'.read_register(node_id=9+x, register_index=0x04))
            asyncio.run(f'esc{x}'.receive_data())
            data = f'esc{x}'.get_data()
            self.superDictionary.append(data)

        return self.superDictionary
    '''
    async def esc_task(self, esc, node_id):

        await esc.send_command(node_id=node_id, command=0x01)
        await esc.read_register(node_id=node_id, register_index=0x04)
        await esc.receive_data()

        data = esc.get_data()

        self.superDictionary.append(data)

    async def escRead(self):

        tasks = []

        for x in range(1, self.escCount):

            #esc = getattr(self, f'esc{x}')
            tasks.append(self.esc_task(self.esc[x], node_id= 9 + x))
        
        await asyncio.gather(*tasks)

        return self.superDictionary

