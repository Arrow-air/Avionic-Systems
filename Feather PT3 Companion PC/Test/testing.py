import multiprocessing
import time
import pygame,math
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 500
window_height = 500


class D1:
    def __init__(self,modeselect:str, display_num):
        #self.display = display
        self.mode = {0:'GCS',1:'FUI'}
        self.modeselect = modeselect

        if self.modeselect == self.mode.get(0):
            self.screen = pygame.display.set_mode((1860,1020), display=display_num)
            print(self.modeselect)
        elif self.modeselect == self.mode.get(1):
            self.screen = pygame.display.set_mode((1280,800) ,display=display_num)
            print(self.modeselect)

        pygame.display.set_caption('UI Window D1')
        #self.display.set_icon(image.load('arrow-lockup-blue.png'))

        self.font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//30))
        self.medium_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//25))
        self.bigger_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//15))

        print('Display No: ' + str(pygame.display.get_num_displays()))
        print('Display Size: ' + str(pygame.display.get_window_size()))
        print('Screen size: ' + str(self.screen.get_size()))
        # both next 2 variable will be updated in the D1_func
        self.parameters = {
        }
        self.parameters_value_range = { # this is how much can the parameters move, if one has a range of -100 to 100 the value here will be 200
            "airspeed_KTS":60
        }

        self.images = {
            "compass":pygame.transform.smoothscale(pygame.image.load("images//compass.png"),(self.screen.get_height()//3.5*1.2,self.screen.get_height()//3.5*1.2)),
            "roll":pygame.transform.smoothscale(pygame.image.load("images//roll image.png"),(self.screen.get_height()//3.5*1.2,self.screen.get_height()//3.5*1.2)),
            "pointer above roll":pygame.image.load("images//pointer above roll.png"),
            "pointer":pygame.image.load("images//pointer.png")
        }
        roll_pointer_ratio = self.images["pointer above roll"].get_height() / self.images["pointer above roll"].get_width()
        self.images["pointer above roll"] = pygame.transform.smoothscale(self.images["pointer above roll"], (self.screen.get_height()//3.5,self.screen.get_height()//3.5*roll_pointer_ratio))
        self.images["pointer"] = pygame.transform.smoothscale(self.images["pointer"], (self.images["compass"].get_width()//10,self.images["compass"].get_width()//10))
    
    def check_for_warning(self):
        warning_variables = []

        for key, value in self.parameters.items():
            if key.endswith('_KTS'):
                if abs(value) >= 55 and abs(value) <= 60:
                    warning_variables.append(key)
            elif key.endswith('_temp_C'):
                if value >= 80 and value <= 180:
                    warning_variables.append(key)
            elif key.endswith('_soc_PCT'):
                if value >= 1 and value <= 15:
                    warning_variables.append(key)
            elif key.endswith('_rpm_PCT'):
                if value >= 120 and value <= 140:
                    warning_variables.append(key)
            elif key == 'OAT':
                if value >= 30 and value <= 100:
                    warning_variables.append(key)
        #for i in range(0,len(warning_variables)):
        #    warning_variables[i] = "Warning: " + warning_variables[i] + " has exceeded tolerance!"
        return warning_variables

    def background(self):
        self.screen.fill((65, 95, 255))
    def draw_transparent_rect(self,win,size,alpha_level,color,pos, border_width = None, border_radius=5):
        transparent_surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        if border_width == None:
            pygame.draw.rect(transparent_surface,(color[0],color[1],color[2],alpha_level) , (0, 0, size[0], size[1]), border_radius=border_radius)
        else:
            pygame.draw.rect(transparent_surface,(color[0],color[1],color[2],alpha_level) , (0, 0, size[0], size[1]), border_width, border_radius=border_radius)
        win.blit(transparent_surface, (pos[0],pos[1]))

    def draw(self):
        self.background()
        self.screen.blit(self.font.render("D1",True,(255,255,255)),(100,100))


def D1_func(parameters_dict, display_num):
    # create the class of the window
    D1_ui = D1("FUI",display_num)
    # update the class parameters
    D1_ui.parameters = parameters_dict

    running = True
    i = 0
    while running:
        D1_ui.parameters = parameters_dict

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        D1_ui.draw()
        i += 1
        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

class D2:
    def __init__(self,modeselect:str,display_num):
        #self.display = display
        self.mode = {0:'GCS',1:'FUI'}
        self.modeselect = modeselect

        if self.modeselect == self.mode.get(0):
            self.screen = pygame.display.set_mode((1860,1020), display=display_num)
            print(self.modeselect)
        elif self.modeselect == self.mode.get(1):
            self.screen = pygame.display.set_mode((1280,800) ,display=display_num)
            print(self.modeselect)

        pygame.display.set_caption('UI Window D2')
        #self.display.set_icon(image.load('arrow-lockup-blue.png'))

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
        self.screen.blit(self.font.render("D2",True,(255,255,255)),(100,100))

def D2_func(parameters_dict,display_num):
    # create the class of the window
    D2_ui = D2("FUI",display_num)
    # update the class parameters
    D2_ui.parameters = parameters_dict

    running = True
    while running:
        D2_ui.parameters = parameters_dict

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        D2_ui.draw()

        # Update the display
        pygame.display.update()

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
    "latitude":"""40° 26' 46" N""",
    "longitude":"""79° 58' 56" W""",
    "flight_time":"38:15",
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

    "BAT1_soc_PCT":90, # the percentage of the battery left, warning range: 1-15
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
}

# Controller function to manage both functions using multiprocessing
def controller():
    manager = multiprocessing.Manager()
    params_dict = manager.dict(parameters)

    # Create separate processes for func1 and func2
    process1 = multiprocessing.Process(target=D1_func, args=(params_dict,0,))
    process2 = multiprocessing.Process(target=D2_func, args=(params_dict,1,))

    # Start both processes
    process1.start()
    process2.start()
    
    # actions that will happen while the processors run
    # change the param_dict which is the shared dict between the processors in order to have the values changed
    
    # Wait for both processes to finish
    process1.join()
    process2.join()

if __name__ == "__main__":
    controller()
