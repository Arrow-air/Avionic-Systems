import serial
import time
import threading

class LoRa:
    
    def __init__(self,LoRaport,LoRabitrate,modeselect):

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        self.LoRaport = LoRaport
        self.LoRabitrate = LoRabitrate
        self.Data = ''
        self.packet = bytes('', 'ascii')

        self.LoRaSerial =  serial.Serial(self.LoRaport,self.LoRabitrate,timeout = 1) # connect to the LoRa Modules 's serial port
        #self.LoRaSerial.set_buffer_size(rx_size=10000,tx_size=10000)

        self.tlock = threading.Lock()

        print("Lora Init")

    def LoRaTransmit(self):
        with self.tlock:
            self.LoRaSerial.write(self.packet)
        time.sleep(0.2)
    
    def LoRaReceive(self):
            
        self.Dataleft = self.LoRaSerial.inWaiting()
        
        while self.Dataleft > 0:
            self.Data = self.LoRaSerial.read()
            time.sleep(0.01)
            self.Dataleft = self.LoRaSerial.inWaiting()
            self.Data += self.LoRaSerial.read(self.Dataleft)
            
        return self.Data

    ''' Lora Configuration Commands
        'ATE\r\n'                                               #Enable/disable AT command echo
        'AT+VER\r\n'                                            #Check the software version number
        'AT+SF=7\r\n'                                           #Set the spreading factor to 7, the value range is 7~12
        'AT+CR=1\r\n'                                           #Set the encoding rate to 1, 1 represents 4/5, 2 represents 4/6, 3 represents 4/7, 4 represents 4/8
        'AT+NETID=0\r\n'                                        #Network ID assignment, the value range is 0~65535
        'AT+LBT=0\r\n'                                          #Enable/disable LBT function, 0: disable, 1: enable
        'AT+TXCH=18\r\n'                                        #Transmit channel, value range 0~80, corresponding frequency point is 850~930MHz or 410~490MHz
        'AT+RXCH=18\r\n'                                        #Receive channel, value range 0~80, corresponding frequency point is 850~930MHz or 410~490MHz
        'AT+ADDR=0\r\n'                                         #Set DTU address, value range 0~65535
        'AT+PORT=3\r\n'                                         #Set COM port, 1:RS422, 2:RS485, 3:RS232
        'AT+BAUD=115200\r\n'                                    #Set COMx port baud rate, value range 1200~115200, 1200, 2400, ....., 57600, 115200ss
        'AT+COMM="8N1"\r\n'                                     #Set COM port parameters, data bits: 8 or 9, parity: N, O, E, stop bits: 0, 1, 2
        'AT+KEY=0\r\n'                                          #Set the key, the value range is 0~65535, 0: prohibit encryption, 1~65535: encrypt the transmission key value
        'AT+AllP=7,125,1,22,0,0,1,18,18,0,0,3,115200, "8N1",0'  #Set the spreading factor to key multi-parameter
        'AT+RESTORE=0\r\n'                                      #Restore factory settings, 0: disabled, 1: enabled
    ''' 
    def LoRaconfig(self):
        self.ATStart = "+++\r\n".encode()                                              #Enter AT command mode
        self.ATExit = "AT+EXI\r\n".encode()                                           #Exit AT command mode
        self.ATE = "ATE\r\n".encode()                                               #Enable/disable AT command echo
        self.ATRSSI ="AT+RSSI=1\r\n".encode()                                         #Enable/disable RSSI signal value output, 0: disable, 1: enable
        self.ATHelp = "AT+HELP\r\n".encode()                                           #View AT help
        self.ATMode = "AT+MODE=1\r\n".encode()                                         #DTU working mode, 1: stream mode, 2: packet mode, 3: relay mode
        self.ATPWR = "AT+PWR=22\r\n".encode()                                         #Set the RF power, the value range is 10~22dBm
        self.ATBW = "AT+BW=2\r\n".encode()                                           #Set bandwidth, 0 means 125KHz, 1 means 250KHz, 2 means 500KHz

        self.packet = self.ATStart
        print(self.packet)
        self.LoRaTransmit()

        self.packet = self.ATMode #+ self.ATE + self.ATPWR + self.ATBW + self.ATRSSI + self.ATExit
        print(self.packet)
        self.LoRaTransmit()

        self.packet = self.ATE
        print(self.packet)
        self.LoRaTransmit()

        self.packet =  self.ATPWR
        print(self.packet)
        self.LoRaTransmit()

        self.packet = self.ATBW
        print(self.packet)
        self.LoRaTransmit()

        self.packet = self.ATRSSI
        print(self.packet)
        self.LoRaTransmit()

        self.packet = self.ATExit
        print(self.packet)
        self.LoRaTransmit()

    def LoraTerminate(self):
        self.LoRaSerial.close()
