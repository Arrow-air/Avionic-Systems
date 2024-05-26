import socket
import os
import time

class TCP:

    def __init__(self,TCP_IP,TCP_PORT,TCP_Buffer,modeselect) -> None:

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        self.headersize = 16

        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.TCP_Buffer = TCP_Buffer

        self.packet = bytes('', 'ascii') 
        self.data = bytes('', 'ascii')

        self.clientsocket = ''
        self.addr = ''

        self.socket = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP
        
        if self.modeselect == self.mode.get(1):
            self.filesocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                os.remove("/tmp/socketname")
            except OSError:
                pass

            self.filesocket.bind("/tmp/socketname")
            self.filesocket.listen(1)
            self.fileclientsocket, self.fileaddr = self.filesocket.accept()     # Establish connection with client.

            self.filesocket1 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            try:
                os.remove("/tmp/socketname1")
            except OSError:
                pass

            self.filesocket1.bind("/tmp/socketname1")
            self.filesocket1.listen(1)
            self.fileclientsocket1, self.fileaddr1 = self.filesocket1.accept()     # Establish connection with client.

            self.socket.bind((self.TCP_IP, self.TCP_PORT))        # Bind to the port
            self.socket.listen(5)                 # Now wait for client connection.
            self.clientsocket, self.addr = self.socket.accept()     # Establish connection with client.

        if self.modeselect == self.mode.get(0):

            self.socket.connect((self.TCP_IP,self.TCP_PORT))  
            
        print("TCP Init")
    
    def TCPServer(self):
        self.msg  = f'{len(self.packet):<{self.headersize}}' + self.packet 
        self.clientsocket.send(self.msg.encode("utf-8"))
        self.fileclientsocket.send(self.msg.encode("utf-8"))
        self.fileclientsocket1.send(self.msg.encode("utf-8"))
        time.sleep(0.05)
            
    def TCPClient(self):

        self.full_msg = ''
        self.new_msg = True

        while True:

            self.rcmsg = self.socket.recv(8192)

            if self.new_msg:

                #print(f"Message Length: {self.rcmsg[:self.headersize]}")
                self.a = f"{self.rcmsg[:self.headersize]}"
                self.msglenprim = self.a.split('\'')[1]
                try:
                 self.msglenprim = self.msglenprim[0]+self.msglenprim[1]+self.msglenprim[2]+self.msglenprim[3]
                except:
                 pass
                #print(self.msglenprim)
                try:
                 self.msglen = int(self.msglenprim)
                except:
                 self.msglen = 1070
                #print(self.msglen)
                self.new_msg = False

            self.full_msg += self.rcmsg.decode("utf-8")

            if len(self.full_msg) - self.headersize == self.msglen:

                self.returnmsg = self.rcmsg[self.headersize:].decode("utf-8")
                #print("Message: ",self.returnmsg)
                self.new_msg = True
                self.full_msg = ''
                
                return self.returnmsg
    
    def TCPReceive(self):
        self.TCPClient()

    def TCPTerminate(self):
        self.socket.close()
