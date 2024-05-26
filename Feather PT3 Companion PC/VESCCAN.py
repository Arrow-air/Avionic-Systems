import can
import struct

class VESCCAN:
    def __init__(self):

        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan') # socketcan_native Bitrate implicit at 500K

        self.id = ''
        self.data = ''
        self.unit_id = ''
        self.command = ''
        self.message = ''

        self.idData = {}
        self.msgData = {}

    def calculate_can_id(self,unit_id, command):

        # Ensure controller ID and command number are within valid range
        if unit_id < 0 or unit_id > 255:
            raise ValueError("Controller ID must be between 0 and 255.")
        if command < 0 or command > 255:
            raise ValueError("Command number must be between 0 and 255.")
        
        # Frame type for data frame is 0
        frame_type = 0

        # Calculate the CAN ID by shifting and combining the parts
        self.id = ( frame_type << 26) | (command << 8) | unit_id
        
        return self.id
    
    def decode_can_id(self,id):

        if id < 0 or id > 0x1FFFFFFF:
            raise ValueError("CAN ID must be a 29-bit value between 0 and 0x1FFFFFFF.")

        # Extract components from the CAN ID
        self.unit_id = id & 0xFF

        self.command = (id >> 8) & 0xFF

        self.spare = (id >> 16) & 0x3FF

        self.frame_type = (id >> 26) & 0x7

        self.idData = {'controller_id': self.unit_id,'command_number': self.command,'spare': self.spare,'frame_type': self.frame_type}

        return self.idData
    
    def read_frame(self):

        self.message = self.can0.recv()

        self.id = self.message.arbitration_id

        if self.message is None:
            return None
        
        if self.message.is_extended_id:
            self.decode_can_id(self.id)
        else:
            self.unit_id = self.id & 0xFF
            self.command = (self.id >> 5) & 0xFF

        self.data = self.message.data

        return self.parse_frame(self.command, self.data, self.unit_id)

    def parse_frame(self, command, data, unit_id):

        self.msgData = {'unit_id': unit_id}

        if command == 0x2B1A:  # CAN_PACKET_BMS_TEMPS
            self.msgData['NoOfCells'] = data[1]
            self.msgData['auxVoltagesIndividual1'] = struct.unpack('>H', data[2:4])[0] * 0.01
            self.msgData['auxVoltagesIndividual2'] = struct.unpack('>H', data[4:6])[0] * 0.01
            self.msgData['auxVoltagesIndividual3'] = struct.unpack('>H', data[6:8])[0] * 0.01

        elif command == 0x260A:  # CAN_PACKET_BMS_V_TOT
            self.msgData['packVoltage'] = struct.unpack('>I', data[0:4])[0]
            self.msgData['chargerVoltage'] = struct.unpack('>I', data[4:8])[0]

        elif command == 0x271A:  # CAN_PACKET_BMS_I
            self.msgData['packCurrent1'] = struct.unpack('>I', data[0:4])[0]
            self.msgData['packCurrent2'] = struct.unpack('>I', data[4:8])[0]

        elif command == 0x280A:  # CAN_PACKET_BMS_AH_WH
            self.msgData['Ah_Counter'] = struct.unpack('>I', data[0:4])[0]
            self.msgData['Wh_Counter'] = struct.unpack('>I', data[4:8])[0]

        elif command == 0x291A:  # CAN_PACKET_BMS_V_CELL
            self.msgData['cellPoint'] = data[0]
            self.msgData['NoOfCells'] = data[1]
            self.msgData['cellVoltage10'] = struct.unpack('>H', data[2:4])[0] * 0.001
            self.msgData['cellVoltage11'] = struct.unpack('>H', data[4:6])[0] * 0.001
            self.msgData['cellVoltage12'] = struct.unpack('>H', data[6:8])[0] * 0.001

        elif command == 0x2A7A:  # CAN_PACKET_BMS_BAL
            self.msgData['NoOfCells'] = data[0]
            self.msgData['bal_state'] = struct.unpack('<Q', data[1:8])[0]

        elif command == 0x2D1A:  # CAN_PACKET_BMS_SOC_SOH_TEMP_STAT
            self.msgData['cellVoltageLow'] = struct.unpack('>H', data[0:2])[0] * 0.001
            self.msgData['cellVoltageHigh'] = struct.unpack('>H', data[2:4])[0] * 0.001
            self.msgData['SOC'] = data[4] * 0.392156862745098
            self.msgData['SOH'] = data[5] * 0.3922
            self.msgData['tBattHi'] = data[6]
            self.msgData['BitF'] = data[7]

        elif command == 0x2C1A:  # CAN_PACKET_BMS_HUM
            self.msgData['CAN_PACKET_BMS_TEMP0'] = struct.unpack('>H', data[0:2])[0] * 0.01
            self.msgData['CAN_PACKET_BMS_HUM_HUM'] = struct.unpack('>H', data[2:4])[0] * 0.01
            self.msgData['CAN_PACKET_BMS_HUM_TEMP1'] = struct.unpack('>H', data[4:6])[0] * 0.01

        else:
            self.msgData['raw_data'] = data

        return self.msgData