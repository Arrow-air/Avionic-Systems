import CyphalCAN
import asyncio

class ESC:

    def __init__(self,modeselect) -> None:

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        
        self.packet = {}

        self.esc1 = CyphalCAN(10)
        self.esc2 = CyphalCAN(11)
        self.esc3 = CyphalCAN(12)
        self.esc4 = CyphalCAN(13)
        self.esc5 = CyphalCAN(14)
        self.esc6 = CyphalCAN(15)

        # asyncio.run(esc.send_command(node_id=10, command=0x01))
        # asyncio.run(esc.read_register(node_id=10, register_index=0x04))
        # asyncio.run(esc.receive_data())
        # data = esc.get_data()
        print("ESC Init")

    def packetStruct(self):
        return self.packet
    
    def escRead(self):
        pass

