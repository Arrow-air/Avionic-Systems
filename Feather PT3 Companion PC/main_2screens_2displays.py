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
        self.screen.blit( self.bigger_font.render( str(self.parameters["airspeed_KTS"]), True,(255,255,255) ) , (self.bigger_font.size("5")[0]//2,speed_text_y))
        self.screen.blit( self.font.render( "kt/s", True,(255,255,255) ) , (self.bigger_font.size("5")[0]//2,speed_text_y + self.bigger_font.size("5")[1]))

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

        # the joysticks + flight time
        # left joystick
        joystick_size = self.screen.get_height()//5
        joystick_width = joystick_size//10
        joystick_x = joystick_size*2
        joystick_y = self.screen.get_height() - joystick_size
        self.draw_transparent_rect(self.screen,(joystick_size,joystick_width),100,(255,255,255),(joystick_x,joystick_y))
        self.draw_transparent_rect(self.screen,(joystick_size,joystick_width),200,(255,255,255),(joystick_x,joystick_y),2)
        self.draw_transparent_rect(self.screen,(joystick_width,joystick_size),100,(255,255,255),(joystick_x + joystick_size//2 - joystick_width//2,joystick_y - joystick_size//2 + joystick_width//2))
        self.draw_transparent_rect(self.screen,(joystick_width,joystick_size),200,(255,255,255),(joystick_x + joystick_size//2 - joystick_width//2,joystick_y - joystick_size//2 + joystick_width//2),2)
        circle_x = joystick_x + joystick_size//2 + joystick_size //2 * (self.parameters["command_yaw"])
        circle_y = joystick_y + joystick_width//2 - joystick_size //2 * (self.parameters["command_throttle"])
        gfxdraw.filled_circle(self.screen, int(circle_x), int(circle_y),joystick_width,(255,255,255,100))
        gfxdraw.filled_circle(self.screen, int(circle_x), int(circle_y),joystick_width//2,(255,255,255,255))
        pygame.draw.circle(self.screen,(255,255,255),(int(circle_x), int(circle_y)),joystick_width,1)
        self.screen.blit(self.medium_font.render("Y",True,(255,255,255)), (joystick_x - self.medium_font.size("Y")[0]*1.5, joystick_y))
        self.screen.blit(self.medium_font.render("T",True,(255,255,255)), (joystick_x + joystick_size//2 - self.medium_font.size("T")[0]//2, joystick_y - joystick_size//2 - self.medium_font.size("T")[0]*1.5))
        
        # flight time, positioned between the joysticks
        time_text = (self.parameters["flight_time"].split(":")[0]+"m") + ":" + (self.parameters["flight_time"].split(":")[1]+"s")
        time_text_x = joystick_x + joystick_size*1.5
        self.screen.blit(self.bigger_font.render(time_text, True, (255,255,255)), (time_text_x, joystick_y))
        self.screen.blit(self.medium_font.render("Flight Time Remaining", True, (255,255,255)), (time_text_x, joystick_y + self.bigger_font.size("1")[1]))

        # right joystick
        joystick_x =  time_text_x + self.medium_font.size("Flight Time Remaining")[0] + joystick_size*0.5 # using the height text position and the time text x and size
        self.draw_transparent_rect(self.screen,(joystick_size,joystick_width),100,(255,255,255),(joystick_x,joystick_y))
        self.draw_transparent_rect(self.screen,(joystick_size,joystick_width),200,(255,255,255),(joystick_x,joystick_y),2)
        self.draw_transparent_rect(self.screen,(joystick_width,joystick_size),100,(255,255,255),(joystick_x + joystick_size//2 - joystick_width//2,joystick_y - joystick_size//2 + joystick_width//2))
        self.draw_transparent_rect(self.screen,(joystick_width,joystick_size),200,(255,255,255),(joystick_x + joystick_size//2 - joystick_width//2,joystick_y - joystick_size//2 + joystick_width//2),2)
        circle_x = joystick_x + joystick_size//2 + joystick_size //2 * (self.parameters["command_roll"])
        circle_y = joystick_y + joystick_width//2 - joystick_size //2 * (self.parameters["command_pitch"])
        gfxdraw.filled_circle(self.screen, int(circle_x), int(circle_y),joystick_width,(255,255,255,100))
        gfxdraw.filled_circle(self.screen, int(circle_x), int(circle_y),joystick_width//2,(255,255,255,255))
        pygame.draw.circle(self.screen,(255,255,255),(int(circle_x), int(circle_y)),joystick_width,1)
        self.screen.blit(self.medium_font.render("R",True,(255,255,255)), (joystick_x - self.medium_font.size("Y")[0]*1.5, joystick_y))
        self.screen.blit(self.medium_font.render("P",True,(255,255,255)), (joystick_x + joystick_size//2 - self.medium_font.size("T")[0]//2, joystick_y - joystick_size//2 - self.medium_font.size("T")[0]*1.5))

        # latitude and longitude text
        position_in_angle_text_pos = (5, joystick_y - joystick_size*2)
        self.screen.blit(self.medium_font.render("Lat: " + self.parameters["latitude"], True, (255,255,255)),(position_in_angle_text_pos[0],position_in_angle_text_pos[1]-self.medium_font.size("L")[1]))
        self.screen.blit(self.medium_font.render("Long: " + self.parameters["longitude"], True, (255,255,255)),(position_in_angle_text_pos[0],position_in_angle_text_pos[1]+self.medium_font.size("L")[1]))
        
        # rotate forward representation, attitude pitch
        pitch_angle = self.parameters["attitude_pitch"]
        line_size = (self.images["compass"].get_width()//3*1.2, self.images["compass"].get_width()//3//8)
        pitch_x = position_in_angle_text_pos[0] +self.medium_font.size("Long: " + self.parameters["longitude"]+"AA")[0] #line_size[0]
        pitch_y = joystick_y - joystick_size*2
        # define and draw the rect around it
        rect_around_pitch_size = (line_size[0]*2, line_size[0]*3)
        self.draw_transparent_rect(self.screen, rect_around_pitch_size,200,(255,255,255), (pitch_x, pitch_y-rect_around_pitch_size[1]//2), 1)
        # draw the text above it that states what it is
        self.screen.blit(self.medium_font.render("Attitude Pitch",True,(255,255,255)),(pitch_x, pitch_y-rect_around_pitch_size[1]//2 - self.medium_font.size("A")[1]*1.1))
        # drawing the lines
        # drawing the lines that shown the angle using the ratio
        closest_above_round = pitch_angle + (10 -(pitch_angle%10)) # closest number above the current angle
        closest_below_round = pitch_angle - (pitch_angle%10) # closest number below the current angle
        space_between_lines = line_size[0]//2
        above_center_y = pitch_y - space_between_lines*((10 -(pitch_angle%10))/10)
        small_lines_x = pitch_x + rect_around_pitch_size[0]//2-line_size[0]*0.5//2
        while above_center_y > pitch_y -rect_around_pitch_size[1]//2:
            if above_center_y - line_size[1] > pitch_y -rect_around_pitch_size[1]//2: # if the y of this is in the rect but the text won't be inside we draw only the smaller line
                # longer line
                self.draw_transparent_rect(self.screen, (line_size[0]*0.5, line_size[1]*0.8),100,(255,255,255),(small_lines_x, above_center_y),border_radius=0)
                # angle text
                self.screen.blit(self.font.render(str(closest_above_round),True,(255,255,255)),(small_lines_x-self.font.size("100")[0]*1.2, above_center_y - self.font.size("1")[1]//2))
            # shorter line
            self.draw_transparent_rect(self.screen, (line_size[0]*0.25, line_size[1]*0.8),100,(255,255,255),(small_lines_x+line_size[0]*0.5//2-line_size[0]*0.25//2, above_center_y+space_between_lines//2),border_radius=0)
            above_center_y -= space_between_lines
            closest_above_round += 10
        above_center_y = pitch_y - space_between_lines*((10 -(pitch_angle%10))/10) + space_between_lines
        while above_center_y < pitch_y +rect_around_pitch_size[1]//2:
            if above_center_y + line_size[1] < pitch_y +rect_around_pitch_size[1]//2: # if the y of this is in the rect but the text won't be inside we draw only the smaller line
                # longer line
                self.draw_transparent_rect(self.screen, (line_size[0]*0.5, line_size[1]*0.8),100,(255,255,255),(small_lines_x, above_center_y),border_radius=0)
                # angle text
                self.screen.blit(self.font.render(str(closest_below_round),True,(255,255,255)),(small_lines_x-self.font.size("100")[0]*1.2, above_center_y - self.font.size("1")[1]//2))
            if above_center_y+space_between_lines//2 < pitch_y +rect_around_pitch_size[1]//2:
                # shorter line
                self.draw_transparent_rect(self.screen, (line_size[0]*0.25, line_size[1]*0.8),100,(255,255,255),(small_lines_x+line_size[0]*0.5//2-line_size[0]*0.25//2, above_center_y+space_between_lines//2),border_radius=0)
            above_center_y += space_between_lines
            closest_below_round -= 10
        # green line in the middle
        pygame.draw.rect(self.screen, (33, 252, 147), [pitch_x + rect_around_pitch_size[0]//2-line_size[0]//2, pitch_y, line_size[0], line_size[1]], border_radius=5)
        # placing the value of it too
        self.screen.blit(self.medium_font.render(str(pitch_angle),True,(255,255,255)),(pitch_x , pitch_y - self.medium_font.size("1")[1]//2))
        
        # roll image showing
        rotated_roll_img = pygame.transform.rotate(self.images["roll"], -self.parameters["attitude_roll"]) # doing minus the angle because pygame rotates to the left side when positive and we need to the right side when positive
        roll_x = pitch_x + rect_around_pitch_size[0]*1.1 + self.images["roll"].get_width()//2 - rotated_roll_img.get_width()//2 # on the right side of the pitch angle representation
        roll_y = pitch_y - rotated_roll_img.get_height()//2 
        self.screen.blit(rotated_roll_img,(roll_x,roll_y))
        self.screen.blit(self.images["pointer above roll"], 
                         (pitch_x + rect_around_pitch_size[0]*1.1 + self.images["roll"].get_width()//2 - self.images["pointer above roll"].get_width()//2,
                           pitch_y - self.images["roll"].get_height()//2 -self.images["pointer above roll"].get_height()//3
                           ))
        # below roll text
        self.screen.blit(self.medium_font.render(str(self.parameters["attitude_roll"]),True, (255,255,255)), 
                         (pitch_x + rect_around_pitch_size[0]*1.1 + self.images["roll"].get_width()//2 - self.medium_font.size(str(self.parameters["attitude_roll"]))[0]//2, 
                          roll_y + rotated_roll_img.get_height()//2 + self.images["roll"].get_height()//2))
        # above roll text
        self.screen.blit(self.medium_font.render("Attitude Roll",True, (255,255,255)), 
                    (pitch_x + rect_around_pitch_size[0]*1.1 + self.images["roll"].get_width()//2 - self.medium_font.size("Attitude Roll")[0]//2,
                    pitch_y - self.images["roll"].get_height()//2 -self.images["pointer above roll"].get_height()//3 - self.medium_font.size("A")[1]
                    ))
        # compass image showing
        rotated_compass = pygame.transform.rotate(self.images["compass"], self.parameters["compass"])
        compass_x = pitch_x + self.images["roll"].get_width()*2 + self.images["compass"].get_width()//2 - rotated_compass.get_width()//2 # on the right side of the roll angle representation
        compass_y = roll_y + rotated_roll_img.get_height()//2 - rotated_compass.get_height()//2  #self.screen.get_height()//2 - rotated_compass.get_height()//2
        self.screen.blit(rotated_compass,(compass_x,compass_y))
        self.screen.blit(self.images["pointer"],
                         (pitch_x + self.images["roll"].get_width()*2 + self.images["compass"].get_width()//2 - self.images["pointer"].get_width()//2,
                          roll_y + rotated_roll_img.get_height()//2 - self.images["compass"].get_height()//2 - self.images["pointer"].get_height()
                          ))
        # below compass text
        self.screen.blit(self.medium_font.render("Compass:"+str(self.parameters["compass"]),True, (255,255,255)), 
                         (pitch_x + self.images["roll"].get_width()*2 + self.images["compass"].get_width()//2 - self.medium_font.size("Compass:"+str(self.parameters["compass"]))[0]//2, 
                          roll_y + rotated_roll_img.get_height()//2 + self.images["compass"].get_height()//2))
        self.screen.blit(self.medium_font.render("Heading:"+str(self.parameters["heading"]),True, (255,255,255)), 
                         (pitch_x + self.images["roll"].get_width()*2 + self.images["compass"].get_width()//2 - self.medium_font.size("Heading:"+str(self.parameters["heading"]))[0]//2, 
                          roll_y + rotated_roll_img.get_height()//2 + self.images["compass"].get_height()//2 + self.medium_font.size("C")[1]))
        # above compass text
        self.screen.blit(self.medium_font.render("Compass",True, (255,255,255)), 
                         (pitch_x + self.images["roll"].get_width()*2 + self.images["compass"].get_width()//2 - self.medium_font.size("Compass")[0]//2,
                          roll_y + rotated_roll_img.get_height()//2 - self.images["compass"].get_height()//2 - self.images["pointer"].get_height()*2
                          ))


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
