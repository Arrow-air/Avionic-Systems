import socket 

TCP_IP = socket.gethostname() #'192.168.1.84'#socket.gethostname() #"127.0.0.1"
print(TCP_IP)
TCP_PORT = 1234
headersize = 16


socketc = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP 

socketc.connect((TCP_IP,TCP_PORT)) 

while True:
    full_msg = ''
    new_msg = True
    while True:
        rcmsg = socketc.recv(2048) 
        if new_msg:
            print(f"Message Length: {rcmsg[:headersize]}")
            msglen = int(rcmsg[:headersize])
            new_msg = False
        full_msg += rcmsg.decode("utf-8")
        if len(full_msg) - headersize == msglen:
            print("Message: ",rcmsg[headersize:].decode("utf-8"))
            new_msg = True
            full_msg = ''
    #print