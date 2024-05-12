import serial
import socket
import time

class UDP:

    def __init__(self) -> None:
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005
        MESSAGE = b"Hello, World!"
            
        print("UDP target IP: %s" % UDP_IP)
        print("UDP target port: %s" % UDP_PORT)
        print("message: %s" % MESSAGE)
        
        sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_DGRAM) # UDP
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

    def UDPTransmit(self):
        pass
    
    def UDPReceive(self):
        pass