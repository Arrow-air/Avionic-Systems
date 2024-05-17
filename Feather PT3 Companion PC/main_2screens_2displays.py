import multiprocessing
import time
import pygame

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 500
window_height = 500


class D1:
    def __init__(self,modeselect:str):
        #self.display = display
        self.mode = {0:'GCS',1:'FUI'}
        self.modeselect = modeselect

        if self.modeselect == self.mode.get(0):
            self.screen = pygame.display.set_mode((1860,1020), display=0)
            print(self.modeselect)
        elif self.modeselect == self.mode.get(1):
            self.screen = pygame.display.set_mode((1280,800) ,display=0)
            print(self.modeselect)

        pygame.display.set_caption('UI Window D1')
        #self.display.set_icon(image.load('arrow-lockup-blue.png'))

        self.font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//35))
        self.bigger_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//20))

        print('Display No: ' + str(pygame.display.get_num_displays()))
        print('Display Size: ' + str(pygame.display.get_window_size()))
        print('Screen size: ' + str(self.screen.get_size()))
        # both next 2 variable will be updated in the UI class
        self.parameters = {
            "altitude_AGL":0,
            "altitude_AGL_set":0,
            "altitude_ABS":0,
            "heading":0,
            "compass":0,
            "attitude_pitch":0,
            "attitude_roll":0,
            "vertical_speed_KTS":0,
            "airspeed_KTS":55, # warning range: 55-60,-60-(-55), [kts], speed will be between 0-60 knots
            "OAT":0, # warning range: 30-max=100
            "command_pitch":0,
            "command_roll":0,
            "command_yaw":0,
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

            "BAT1_soc_PCT":0, # warning range: 1-15
            "BAT2_soc_PCT":0, # warning range: 1-15
            "BAT3_soc_PCT":0, # warning range: 1-15
            "BAT4_soc_PCT":0, # warning range: 1-15
            "BAT5_soc_PCT":0, # warning range: 1-15
            "BAT6_soc_PCT":0, # warning range: 1-15

            "MOT1_rpm_PCT":130, # warning range: 120-max=140
            "MOT2_rpm_PCT":130, # warning range: 120-max=140
            "MOT3_rpm_PCT":130, # warning range: 120-max=140
            "MOT4_rpm_PCT":130, # warning range: 120-max=140
            "MOT5_rpm_PCT":130, # warning range: 120-max=140
            "MOT6_rpm_PCT":130, # warning range: 120-max=140

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
        self.parameters_value_range = { # this is how much can the parameters move, if one has a range of -100 to 100 the value here will be 200
            "airspeed_KTS":60
        }
    
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
        self.screen.fill("blue")
    def draw_transparent_rect(self,win,size,alpha_level,color,pos, border_width = None):
        transparent_surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        if border_width == None:
            pygame.draw.rect(transparent_surface,(color[0],color[1],color[2],alpha_level) , (0, 0, size[0], size[1]), border_radius=5)
        else:
            pygame.draw.rect(transparent_surface,(color[0],color[1],color[2],alpha_level) , (0, 0, size[0], size[1]), border_width, border_radius=5)
        win.blit(transparent_surface, (pos[0],pos[1]))

    def draw(self):
        self.background()
        # show the warnings
        # warning are on the right screen(right part of the window)(D2)
        warnings = self.check_for_warning()
        if warnings != []:
            warnings = ", ".join(warnings)
            text = "Warning: " + warnings + " has exceeded tolerance!"

            max_text_width = self.screen.get_width()//5*4
            x =  self.screen.get_width() - max_text_width - self.bigger_font.size("5")[0] # the warnings are on the right part of the second screen(D2), doing minus the size of 5 because there are the lines of the height and this is how they are made
            y = 20 # leaving space for the speed text

            current_text = ""
            text_lines = []
            # splitting the text into lines because it is too long for 1 line sometimes
            for word in text.split(" "):
                # if text is too long
                if self.font.size(current_text+" " + word)[0] > max_text_width:
                    text_lines.append(current_text)
                    current_text = word
                # if text is not too long
                else:
                    current_text += word + " "
                    if word == text.split(" ")[-1]:
                        text_lines.append(current_text)

            max_length_text = max(text_lines, key=len)
            if max_length_text[-1] == " ":
                max_length_text = max_length_text[:-1]

            # drawing the square behind the text
            pygame.draw.rect(self.screen,(200,200,200),[x - self.font.size("a")[0],y,  # x, y
                                                        max_text_width, # width
                                                        (len(text_lines)+1)*(self.font.size("A")[1]) # height
                                                        ],
                             border_top_left_radius = 10, border_top_right_radius = 10, border_bottom_left_radius = 10, border_bottom_right_radius = 10) # round corners with the radius of 10
            pygame.draw.rect(self.screen,(0,0,0),[x - self.font.size("a")[0],y, # x,y
                                                max_text_width, # width
                                                (len(text_lines)+1)*(self.font.size("A")[1]) # height
                                                ],2, # width of the line of the rect(rect of only outer line)
                                                10,10,10,10) # round corners with the radius of 10
            y += self.font.size("a")[1]//2 # adding to the y for it to look better
            # blit text by lines and y changes
            for line_text in text_lines:
                self.screen.blit(self.font.render(line_text,True,(0,0,0)),(x,y))
                y += self.font.size("A")[1]

        # aircraft speed:
        # placing the line above the text to show how fast the aircraft is compare to it's max
        speed_bar_x = 0 + self.font.size("a")[0]//2
        speed_bar_width = self.screen.get_width()/20*19
        speed_bar_height = self.font.size("a")[1]//2
        self.draw_transparent_rect(self.screen,(speed_bar_width,speed_bar_height),100,(200,200,200),(speed_bar_x,5))
        self.draw_transparent_rect(self.screen,(speed_bar_width,speed_bar_height),100,(255,255,255),(speed_bar_x,5),1)
        pygame.draw.rect(self.screen, (255,255,255), [speed_bar_x, 5, speed_bar_width*(abs(self.parameters["airspeed_KTS"])/ self.parameters_value_range["airspeed_KTS"]), speed_bar_height], border_radius=5)

        # placing the text of the speed with it's units
        speed_text_y = 20
        self.screen.blit( self.bigger_font.render( str(self.parameters["airspeed_KTS"]), True,(0,0,0) ) , (self.bigger_font.size("5")[0]//2,speed_text_y))
        self.screen.blit( self.font.render( "kt/s", True,(0,0,0) ) , (self.bigger_font.size("5")[0]//2,speed_text_y + self.bigger_font.size("5")[1]))

        # aircraft height variables(bar variables):
        num_of_lines = 29 # 1 on the text y, 9 below and 9 above
        line_width = self.bigger_font.size("5")[0]
        line_height = 2
        space_between_lines = self.screen.get_height()//(num_of_lines-1)
        height_lines_y = [self.screen.get_height()//2]
        for y in range(height_lines_y[0],0,-space_between_lines-line_height):
            height_lines_y.append(y)
        for y in range(height_lines_y[0],self.screen.get_height(),+space_between_lines+line_height):
            height_lines_y.append(y)
        lines_x = self.screen.get_width() -  line_width*1.2
        height_lines_y = sorted(height_lines_y)
        # aircraft height text bliting
        self.screen.blit(self.bigger_font.render(str(self.parameters["altitude_AGL"])+"ft", True, (255,255,255)), 
                         (self.screen.get_width() - line_width*2.6 - self.bigger_font.size(str(self.parameters["altitude_AGL"])+"ft")[0],self.screen.get_height()//2 - self.bigger_font.size("f")[1]//2)
                         )
        # aircraft height bar
        a = 0 # the alpha level(transparency value)
        a_goes_up = True
        for line_y in height_lines_y:
            if line_y == self.screen.get_height()//2: # if the middle line(the one which is on the numbers)
                # drawing a line without alpha level
                pygame.draw.rect(self.screen, (255,255,255,255), [lines_x - line_width,line_y,line_width*2,line_height])
                a_goes_up = False
            else: # the lines with the alpha level
                self.draw_transparent_rect(self.screen, (line_width,line_height),a,(255,255,255),(lines_x,line_y))
                # if it is above the middle line
                if a_goes_up == True: # will add to the alpha level by the number of lines
                    a += 255//((num_of_lines-2)//2)
                    if a > 255:
                        a = 255
                # if it is below the middle line
                else: # will decrease to the alpha level by the number of lines
                    a -= 255//((num_of_lines-2)//2)
                    if a < 0:
                        a = 1

        pygame.display.update()

def D1_func():
    # Create the window
    D1_ui = D1("FUI")
    #window = pygame.display.set_mode((window_width, window_height), display=0)
    #pygame.display.set_caption("D1")

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the window with white color
        #window.fill((255, 255, 255))
        D1_ui.draw()

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

class D2:
    def __init__(self,modeselect:str):
        #self.display = display
        self.mode = {0:'GCS',1:'FUI'}
        self.modeselect = modeselect

        if self.modeselect == self.mode.get(0):
            self.screen = pygame.display.set_mode((1860,1020), display=1)
            print(self.modeselect)
        elif self.modeselect == self.mode.get(1):
            self.screen = pygame.display.set_mode((1280,800) ,display=1)
            print(self.modeselect)

        pygame.display.set_caption('UI Window D2')
        #self.display.set_icon(image.load('arrow-lockup-blue.png'))

        self.font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//35))
        self.bigger_font = pygame.font.SysFont('Corbel', int(self.screen.get_height()//20))

        print('Display No: ' + str(pygame.display.get_num_displays()))
        print('Display Size: ' + str(pygame.display.get_window_size()))
        print('Screen size: ' + str(self.screen.get_size()))
        # both next 2 variable will be updated in the UI class
        self.parameters = {
            "altitude_AGL":0,
            "altitude_AGL_set":0,
            "altitude_ABS":0,
            "heading":0,
            "compass":0,
            "attitude_pitch":0,
            "attitude_roll":0,
            "vertical_speed_KTS":0,
            "airspeed_KTS":55, # warning range: 55-60,-60-(-55), [kts], speed will be between 0-60 knots
            "OAT":0, # warning range: 30-max=100
            "command_pitch":0,
            "command_roll":0,
            "command_yaw":0,
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

            "BAT1_soc_PCT":0, # warning range: 1-15
            "BAT2_soc_PCT":0, # warning range: 1-15
            "BAT3_soc_PCT":0, # warning range: 1-15
            "BAT4_soc_PCT":0, # warning range: 1-15
            "BAT5_soc_PCT":0, # warning range: 1-15
            "BAT6_soc_PCT":0, # warning range: 1-15

            "MOT1_rpm_PCT":130, # warning range: 120-max=140
            "MOT2_rpm_PCT":130, # warning range: 120-max=140
            "MOT3_rpm_PCT":130, # warning range: 120-max=140
            "MOT4_rpm_PCT":130, # warning range: 120-max=140
            "MOT5_rpm_PCT":130, # warning range: 120-max=140
            "MOT6_rpm_PCT":130, # warning range: 120-max=140

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
        self.parameters_value_range = { # this is how much can the parameters move, if one has a range of -100 to 100 the value here will be 200
            "airspeed_KTS":60
        }
    def background(self):
        self.screen.fill("blue")
    def draw(self):
        self.screen.blit(self.bigger_font.render("D2",True,(255,255,255)), (self.screen.get_width()//2, self.screen.get_height()//2))

def D2_func():
    # Create the window
    D2_ui = D2("FUI")
    #window = pygame.display.set_mode((window_width, window_height), display=0)
    #pygame.display.set_caption("D1")

    # Run the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the window with white color
        #window.fill((255, 255, 255))
        D2_ui.draw()

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

# Controller function to manage both functions using multiprocessing
def controller():
    # Create separate processes for func1 and func2
    process1 = multiprocessing.Process(target=D1_func)
    process2 = multiprocessing.Process(target=D2_func)

    # Start both processes
    process1.start()
    process2.start()

    # Wait for both processes to finish
    process1.join()
    process2.join()

if __name__ == "__main__":
    controller()
