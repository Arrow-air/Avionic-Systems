import pycyphal
from pycyphal.transport.can import CANTransport
from pycyphal.application import Node, NodeInfo, NodeHeartbeatPublisher
from pycyphal.transport import MessageDataSpecifier, ServiceDataSpecifier
from pycyphal.transport import PayloadMetadata, TransferFrom, TransferID
import asyncio

class CyphalCAN:
    def __init__(self, node_id: int = 10):

        self.transport = CANTransport(interface='can0', baudrate=500000)

        self.node = Node(self.transport, NodeInfo(), node_id)
        self.esc_data = {}

    async def send_command(self, node_id: int, command: int):
        payload = bytearray([command, 0x00, 0x00])
        await self.node.broadcast(payload, MessageDataSpecifier(6144), priority=1)

    async def read_register(self, node_id: int, register_index: int):
        request_payload = bytearray([0x00, register_index & 0xFF, (register_index >> 8) & 0xFF])
        await self.node.request(node_id, request_payload, ServiceDataSpecifier(256))

    async def write_register(self, node_id: int, register_index: int, value: int):
        request_payload = bytearray([0x02, register_index & 0xFF, (register_index >> 8) & 0xFF, value & 0xFF, (value >> 8) & 0xFF])
        await self.node.request(node_id, request_payload, ServiceDataSpecifier(256))

    async def get_node_info(self, node_id: int):
        await self.node.request(node_id, b'', ServiceDataSpecifier(430))

    async def receive_data(self, timeout: float = 1.0):
        try:
            transfer = await asyncio.wait_for(self.node.receive(), timeout)
            self.parse_message(transfer)
        except asyncio.TimeoutError:
            print("No message received")

    def parse_message(self, transfer: TransferFrom):
        if isinstance(transfer.data_specifier, MessageDataSpecifier):
            if transfer.data_specifier.subject_id in range(6144, 6152):
                self.parse_command_control(transfer.payload)
            elif transfer.data_specifier.subject_id in range(6152, 6160):
                self.parse_throttle_data(transfer.payload)
            elif transfer.data_specifier.subject_id == 6160:
                self.parse_info_upload_6160(transfer.payload)
            elif transfer.data_specifier.subject_id == 6161:
                self.parse_info_upload_6161(transfer.payload)
            elif transfer.data_specifier.subject_id == 7509:
                self.parse_heartbeat(transfer.payload)

    def parse_command_control(self, payload: bytearray):
        command = payload[0]
        node_id = payload[1]
        self.esc_data['command_control'] = {'command': command, 'node_id': node_id}

    def parse_throttle_data(self, payload: bytearray):
        throttles = [int.from_bytes(payload[i:i+2], 'little') for i in range(0, 7, 2)]
        self.esc_data['throttle_data'] = throttles

    def parse_info_upload_6160(self, payload: bytearray):
        electrical_speed = int.from_bytes(payload[0:2], 'little')
        bus_current = int.from_bytes(payload[2:4], 'little', signed=True)
        running_status = int.from_bytes(payload[4:6], 'little')
        self.esc_data['info_upload_6160'] = {
            'electrical_speed': electrical_speed,
            'bus_current': bus_current,
            'running_status': running_status
        }

    def parse_info_upload_6161(self, payload: bytearray):
        output_throttle = int.from_bytes(payload[0:2], 'little')
        bus_voltage = int.from_bytes(payload[2:4], 'little', signed=True)
        temperatures = [payload[i] - 40 for i in range(4, 7)]
        self.esc_data['info_upload_6161'] = {
            'output_throttle': output_throttle,
            'bus_voltage': bus_voltage,
            'temperatures': temperatures
        }

    def parse_heartbeat(self, payload: bytearray):
        power_on_time = int.from_bytes(payload[0:4], 'little')
        health_status = payload[4]
        current_mode = payload[5]
        self.esc_data['heartbeat'] = {
            'power_on_time': power_on_time,
            'health_status': health_status,
            'current_mode': current_mode
        }

    def get_data(self):
        return self.esc_data