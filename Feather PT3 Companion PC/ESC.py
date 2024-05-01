import time
import sys
import os
import can

class ESC:

    def __init__(self) -> None:
        self.packet = [bytes('', 'ascii')]

    def packetStruct(self):
        return self.packet

