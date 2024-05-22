import time
import sys
import os
#import can

class ESC:

    def __init__(self,modeselect) -> None:

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        
        self.packet = ['']
        print("ESC Init")

    def packetStruct(self):
        return self.packet

