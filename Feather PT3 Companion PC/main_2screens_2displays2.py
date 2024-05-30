import time
import pygame,math
from pygame import gfxdraw
import socket
import ast
import threading
from concurrent.futures import ThreadPoolExecutor

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 500
window_height = 500

class D2:
    def __init__(self,modeselect:str,display_num):
        #self.display = display
        self.mode = {0:'GCS',1:'FUI'}
        self.modeselect = modeselect

        self.filesocket1 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.filesocket1.connect("/tmp/socketname1")
        self.headersize = 16
        self.full_msg = ''
        self.new_msg = True

        self.tlock = threading.Lock()

        if self.modeselect == self.mode.get(0):
            self.screen = pygame.display.set_mode((1860,1020), display=display_num)
            print(self.modeselect)
        elif self.modeselect == self.mode.get(1):
            self.screen = pygame.display.set_mode((1860,1020) ,display=display_num)
            print(self.modeselect)

        pygame.display.set_caption('UI Window D2')
        pygame.display.set_icon(pygame.image.load('images/feather-icon.png'))

        self.small_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//40))
        self.medium_small_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//37.5))
        self.font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//35))
        self.bigger_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//20))

        print('Display No: ' + str(pygame.display.get_num_displays()))
        print('Display Size: ' + str(pygame.display.get_window_size()))
        print('Screen size: ' + str(self.screen.get_size()))
        # both next 2 variable will be updated in the D2_func
        self.parameters = {
        }
        self.parameters_value_range = { # this is how much can the parameters move, if one has a range of -100 to 100 the value here will be 200
            
        }
        self.images = {
            "structure":pygame.image.load("images/structure.png"),
            "motor circle":pygame.image.load("images/circle image.png"),
        }
        self.images["structure"] = pygame.transform.smoothscale(self.images["structure"], ((self.images["structure"].get_width()/self.images["structure"].get_height())*self.screen.get_height()//2, self.screen.get_height()//2))
        self.images["motor circle"] = pygame.transform.smoothscale(self.images["motor circle"],(self.images["structure"].get_height()//2.1,self.images["structure"].get_height()//2.1))

    def background(self):
        self.screen.fill((65, 95, 255))

    def draw_circle_info(self, motor_num,x,y,outer_circle_size, text_side):

        # BAT,ESC color
        circle_center = (x + outer_circle_size[0]//2, y + outer_circle_size[1]//2)
        bat_value = self.parameters["BAT"+str(motor_num)+"_temp_C"]
        esc_value = self.parameters["ESC"+str(motor_num)+"_temp_C"]

        # drawing the battery color which is a ring around the motor circle
        battery_percentage = self.parameters["BAT"+str(motor_num)+"_soc_PCT"] / 100 # divide by 100 to get the percentage as a number between 0-1
        battery_ring_color = (255 - int(255*battery_percentage), int(255*battery_percentage),0)

        
        for y2 in range(int(y - outer_circle_size[1]*0.2),int(y+outer_circle_size[1]*1.2)):
            for x2 in range(int(x - outer_circle_size[0]*0.2), int(x+outer_circle_size[0]*1.2)):
                distance_from_center = math.sqrt(math.pow(circle_center[0] - x2,2)+math.pow(circle_center[1] - y2,2))
                if distance_from_center <= outer_circle_size[0]//2:
                    if x2 > circle_center[0]: # ESC
                        temp_to_max_ratio = bat_value/100
                        if temp_to_max_ratio >= 1:
                            temp_to_max_ratio = 1
                        color = (int(255*temp_to_max_ratio), 255 - int(255*temp_to_max_ratio),0)
                        self.screen.set_at((x2,y2),color)
                    else: # BUT
                        temp_to_max_ratio = esc_value/100
                        if temp_to_max_ratio >= 1:
                            temp_to_max_ratio = 1
                        color = (int(255*temp_to_max_ratio), 255 - int(255*temp_to_max_ratio),0)
                        self.screen.set_at((x2,y2),color)
                elif distance_from_center >= outer_circle_size[0]//2 and distance_from_center <=  outer_circle_size[0]*(2.3/4):
                    d_y2_y = y2 - y
                    ratio_to_size = d_y2_y/outer_circle_size[1]
                    if ratio_to_size <= battery_percentage:
                        self.screen.set_at((x2,y2),battery_ring_color)
        self.screen.blit(self.images["motor circle"], (x,y))

        # rpm text
        self.screen.blit(self.small_font.render(str(self.parameters["MOT"+str(motor_num)+"_rpm_PCT"]),True,(0,0,0)), (x + outer_circle_size[0]//2 - self.small_font.size(str(self.parameters["MOT"+str(motor_num)+"_rpm_PCT"]))[0]//2,y + outer_circle_size[1]//2 - self.small_font.size("R")[1]))
        self.screen.blit(self.small_font.render("RPM",True,(100,100,100)), (x + outer_circle_size[0]//2 - self.small_font.size("RPM")[0]//2,y + outer_circle_size[1]//2))
        
        # BAT text
        BAT_text = str(bat_value) + "C"
        self.screen.blit(self.medium_small_font.render(BAT_text,True,(0,0,0)), (x + outer_circle_size[0]//2 - self.medium_small_font.size(BAT_text+"aa.")[0], y + outer_circle_size[1]//2+self.medium_small_font.size("A")[1]*1.1))
        self.screen.blit(self.medium_small_font.render("BAT",True,(0,0,0)), (x + outer_circle_size[0]//2 - self.medium_small_font.size("BAT"+"ab")[0], y + outer_circle_size[1]//2+self.medium_small_font.size("A")[1]*2.1))
        
        # ESC text
        ESC_text = str(esc_value) + "C"
        self.screen.blit(self.medium_small_font.render(ESC_text,True,(0,0,0)), (x + outer_circle_size[0]//2 + self.medium_small_font.size("aa.")[0], y + outer_circle_size[1]//2+self.medium_small_font.size("A")[1]*1.1))
        self.screen.blit(self.medium_small_font.render("ESC",True,(0,0,0)), (x + outer_circle_size[0]//2 + self.medium_small_font.size("ab")[0], y + outer_circle_size[1]//2+self.medium_small_font.size("A")[1]*2.1))

        # the text on the side
        if text_side =='l': # left side of the circle
            text_x = x - self.font.size("Volt: 12345")[0]
            self.screen.blit(self.font.render("Volt: "+str(self.parameters["ESC"+str(motor_num)+"_V"]),True,(255,255,255)), (text_x, y + outer_circle_size[1]//2 - self.font.size("V")[1]))
            self.screen.blit(self.font.render("Cur: "+str(self.parameters["ESC"+str(motor_num)+"_CUR_AMP"]),True,(255,255,255)), (text_x, y + outer_circle_size[1]//2))
            self.screen.blit(self.font.render("Power: "+str(self.parameters["ESC"+str(motor_num)+"_CUR_AMP"]*self.parameters["ESC"+str(motor_num)+"_V"]),True,(255,255,255)), (text_x, y + outer_circle_size[1]//2 + self.medium_small_font.size("P")[1]))
        else: # right side of the circle
            text_x = x + outer_circle_size[0] + self.font.size("45")[0]
            self.screen.blit(self.font.render("Volt: "+str(self.parameters["ESC"+str(motor_num)+"_V"]),True,(255,255,255)), (text_x, y + outer_circle_size[1]//2 - self.font.size("V")[1]))
            self.screen.blit(self.font.render("Cur: "+str(self.parameters["ESC"+str(motor_num)+"_CUR_AMP"]),True,(255,255,255)), (text_x, y + outer_circle_size[1]//2))
            self.screen.blit(self.font.render("Power: "+str(self.parameters["ESC"+str(motor_num)+"_CUR_AMP"]*self.parameters["ESC"+str(motor_num)+"_V"]),True,(255,255,255)), (text_x, y + outer_circle_size[1]//2 + self.medium_small_font.size("P")[1]))
        
    def draw(self):

        self.background()

        structure_size = self.images["structure"].get_size()
        structure_x = self.screen.get_width()//2 - structure_size[0]//2
        structure_y = self.screen.get_height()//2 - structure_size[1]//2
        self.screen.blit(self.images["structure"], (structure_x,structure_y))

        motor_circle_size = self.images["motor circle"].get_size()

        # left top
        x = structure_x - motor_circle_size[0]*0.8
        y = structure_y - motor_circle_size[1]*0.8
        pygame.draw.line(self.screen, (255,255,255), (x+motor_circle_size[0]*0.85,y+motor_circle_size[1]*0.85), (x+motor_circle_size[0]*1.1,y+motor_circle_size[1]*1.1),10)
        self.draw_circle_info(1,x,y,motor_circle_size,'l')

        # left middle
        x = structure_x - motor_circle_size[0]*1.1
        y = structure_y + structure_size[1]//2 - motor_circle_size[1]//2
        pygame.draw.line(self.screen, (255,255,255), (x+motor_circle_size[0]*0.9,y+motor_circle_size[1]//1.4), (x+motor_circle_size[0]*1.11,y+motor_circle_size[1]//1.4),10)
        self.draw_circle_info(3,x,y,motor_circle_size,'l')
        
        # left down
        x = structure_x - motor_circle_size[0]*0.8
        y = structure_y  + structure_size[1] - motor_circle_size[1]//10
        pygame.draw.line(self.screen, (255,255,255), (x+motor_circle_size[0]*0.75,y + motor_circle_size[1]*0.1), (x+motor_circle_size[0]*0.9,y - motor_circle_size[1]*0.1),10)
        self.draw_circle_info(5,x,y,motor_circle_size,'l')

        # right top
        x = structure_x + structure_size[0] - motor_circle_size[0]*0.2
        y = structure_y - motor_circle_size[1]*0.8
        pygame.draw.line(self.screen, (255,255,255), (x+motor_circle_size[0]*0.15,y+motor_circle_size[1]*0.85), (x-motor_circle_size[0]*0.1,y+motor_circle_size[1]*1.1),10)
        self.draw_circle_info(2,x,y,motor_circle_size,'r')

        # right middle
        x = structure_x + structure_size[0] + motor_circle_size[0]*0.1
        y = structure_y + structure_size[1]//2 - motor_circle_size[1]//2
        pygame.draw.line(self.screen, (255,255,255), (x+motor_circle_size[0]*0.1,y+motor_circle_size[1]//1.4), (x-motor_circle_size[0]*0.11,y+motor_circle_size[1]//1.4),10)
        self.draw_circle_info(4,x,y,motor_circle_size,'r')

        # right down
        x = structure_x + structure_size[0] - motor_circle_size[0]*0.2
        y = structure_y  + structure_size[1] - motor_circle_size[1]//10
        pygame.draw.line(self.screen, (255,255,255), (x+motor_circle_size[0]*0.25,y + motor_circle_size[1]*0.1), (x+motor_circle_size[0]*0.1,y - motor_circle_size[1]*0.1),10)
        self.draw_circle_info(6,x,y,motor_circle_size,'r')
        

    def Fileclient(self,parameters_dict):
        while True:

            with self.tlock:
                
                self.rcmsg = self.filesocket1.recv(8192)
                time.sleep(0.01)

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
                    self.dicy = ast.literal_eval(self.returnmsg)
                    self.parameters = self.dicy
                    self.new_msg = True
                    self.full_msg = ''
                    #print(self.parameters)
                    #return self.parameters

def D2_func(gound_or_flight,parameters_dict,display_num):

    # create the class of the window
    D2_ui = D2(gound_or_flight,display_num)

    # update the class parameters
    D2_ui.parameters = parameters_dict

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        dataThread = threading.Thread(target=D2_ui.Fileclient,args=(D2_ui.parameters,),daemon=True)
        dataThread.start()
       
        D2_ui.draw()

        # Update the display
        pygame.display.update()

        # intialise pygame refresh rate and call it clock
        clock = pygame.time.Clock()
        clock.tick(10)

    # Quit Pygame
    pygame.quit()

parameters = {
    "altitude_AGL":0,
    "altitude_AGL_set":0,
    "altitude_ABS":0,
    "heading":0,
    "compass":0,
    "attitude_pitch":0, # forward-backward rotation of the aircraft itself, in what angle the aircraft is leaning to forward or backward, range: -180 to 180(minus is leaning backward, positive is leaning forward)
    "attitude_roll":0, # right-left rotation of the aircraft itself, in what angle the aircraft is leaning side wise, range: -180 to 180(minus is leaning to the left side, positive is to the right side)
    "vertical_speed_KTS":0,
    "airspeed_KTS":0, # warning range: 55-60,-60-(-55), [kts], speed will be between 0-60 knots
    "OAT":0, # warning range: 30-max=100
    "latitude":'40d26a46q',
    'longitude':'79d58a56q',
    "flight_time":'38:15',
    "command_pitch":0, # right joystick, up-down, range: -1 to 1
    "command_roll":0, # right joystick, left-right, range: -1 to 1
    "command_throttle":0, # left joystick, up-down, range: -1 to 1
    "command_yaw":0, # left joystick, left-right, range: -1 to 1
    "switch_states":0,
    "parachute_state":0,

    "BAT1_temp_C":0, # warning range: 80-180
    "BAT2_temp_C":0, # warning range: 80-180
    "BAT3_temp_C":0, # warning range: 80-180
    "BAT4_temp_C":0, # warning range: 80-180
    "BAT5_temp_C":0, # warning range: 80-180
    "BAT6_temp_C":0, # warning range: 80-180

    "ESC1_temp_C":0,
    "ESC2_temp_C":0,
    "ESC3_temp_C":0,
    "ESC4_temp_C":0,
    "ESC5_temp_C":0,
    "ESC6_temp_C":0,

    "MOT1_temp_C":0,
    "MOT2_temp_C":0,
    "MOT3_temp_C":0,
    "MOT4_temp_C":0,
    "MOT5_temp_C":0,
    "MOT6_temp_C":0,

    "BAT1_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
    "BAT2_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
    "BAT3_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
    "BAT4_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
    "BAT5_soc_PCT":100, # the percentage of the battery left, warning range: 1-15
    "BAT6_soc_PCT":100, # the percentage of the battery left, warning range: 1-15

    "MOT1_rpm_PCT":0, # warning range: 120-max=140
    "MOT2_rpm_PCT":0, # warning range: 120-max=140
    "MOT3_rpm_PCT":0, # warning range: 120-max=140
    "MOT4_rpm_PCT":0, # warning range: 120-max=140
    "MOT5_rpm_PCT":0, # warning range: 120-max=140
    "MOT6_rpm_PCT":0, # warning range: 120-max=140

    "ESC1_V":0,
    "ESC2_V":0,
    "ESC3_V":0,
    "ESC4_V":0,
    "ESC5_V":0,
    "ESC6_V":0,
    
    "ESC1_CUR_AMP":0,
    "ESC2_CUR_AMP":0,
    "ESC3_CUR_AMP":0,
    "ESC4_CUR_AMP":0,
    "ESC5_CUR_AMP":0,
    "ESC6_CUR_AMP":0,
    "TimeStamp":0
}

if __name__ == "__main__":

    D2_func("FUI",parameters,1)
