import socket 
from datetime import datetime

TCP_IP = socket.gethostname() #"127.0.0.1"
print(TCP_IP)
TCP_PORT = 1234
headersize = 16


socketc = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_STREAM) # TCP 
socketc.bind((TCP_IP, TCP_PORT))        # Bind to the port
socketc.listen(5)                 # Now wait for client connection.
clientsocket, addr = socketc.accept()     # Establish connection with client.

dataDictionary = {'altitude_AGL':0,'altitude_AGL_set':0,'altitude_ABS':0,'altitude_AGL':0,'heading':0,'compass':0,'attitude_pitch':0,'attitude_roll':0,'vertical_speed_KTS':0,
                               'airspeed_KTS':0,'OAT':0,'altitude_ABS':0,'command_pitch':0,'command_roll':0,'command_yaw':0,'switch_states':0,'parachute_state':0,'BAT1_temp_C':0,
                               'BAT2_temp_C':0,'BAT3_temp_C':0,'BAT4_temp_C':0,'BAT5_temp_C':0,'BAT6_temp_C':0,'ESC1_temp_C':0,'ESC2_temp_C':0,'ESC3_temp_C':0,'ESC4_temp_C':0,
                               'ESC5_temp_C':0,'ESC6_temp_C':0,'MOT1_temp_C':0,'MOT2_temp_C':0,'MOT3_temp_C':0,'MOT4_temp_C':0,'MOT5_temp_C':0,'MOT6_temp_C':0,'BAT1_soc_PCT':0,
                               'BAT2_soc_PCT':0,'BAT3_soc_PCT':0,'BAT4_soc_PCT':0,'BAT5_soc_PCT':0,'BAT6_soc_PCT':0,'MOT1_rpm_PCT':0,'MOT2_rpm_PCT':0,'MOT3_rpm_PCT':0,'MOT4_rpm_PCT':0,
                               'MOT5_rpm_PCT':0,'MOT6_rpm_PCT':0,'ESC1_V':0,'ESC2_V':0,'ESC3_V':0,'ESC4_V':0,'ESC5_V':0,'ESC6_V':0,'ESC1_CUR_AMP':0,
                               'ESC2_CUR_AMP':0,'ESC3_CUR_AMP':0,'ESC4_CUR_AMP':0,'ESC5_CUR_AMP':0,'ESC6_CUR_AMP':0,'TimeStamp':'0'}
while True:
    dataDictionary.__setitem__('TimeStamp',str(datetime.now()))
    packet = str(dataDictionary)
    msg  = f'{len(packet):<{headersize}}' + packet 
    clientsocket.send(msg.encode("utf-8"))
    print("Address: ",addr)
    print("Message: ",msg)