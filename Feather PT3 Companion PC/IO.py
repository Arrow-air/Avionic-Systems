#import Rpi.gpio as gpio
import time

class IO:

    def __init__(self,modeselect) -> None:
        
        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        self.packet = {}
        print("IO Init")

    def readIO(self):
        pass

    def writeIO(self):
        pass

    def analogueReadIO(self):
        pass
    
    def analogueWriteIO(self):
        pass

    def packetStruct(self):
        return self.packet