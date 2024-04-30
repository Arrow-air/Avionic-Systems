import time
import can
import pygame

class Joystick:
    
    def __init__(self) -> None:
        self.old_min = -1
        self.old_max = 1
        self.new_min = 100
        self.new_max = 355
        
        if pygame.joystick.get_init() == True:
            self.USBcontrols = [pygame.joystick.Joystick(id) for id in range(pygame.joystick.get_count())]      # call the joystick controls
            [i.init() for i in self.USBcontrols]                            # initialise the USB controls
            self.controllerName = [str(i.get_name()) for i in self.USBcontrols]
            self.controlleraxesNumber = [i.get_numaxes() for i in self.USBcontrols]
            self.controllerhatNumber = [i.get_numhats() for i in self.USBcontrols]
            self.controllerbuttonNumber = [i.get_numbuttons() for i in self.USBcontrols]

            print(self.controllerName)
        
        '''
        if self.JoyCAN == True:
        
        '''

    def valueMap(self,old_value):
        new_value = str(int(round(( ( old_value - self.old_min ) / (self.old_max - self.old_min) ) * (self.new_max - self.new_min) + self.new_min)))
        return(new_value)
    
    def DOF4ControlUSB(self):
        self.Yaw = Joystick.valueMap(self,self.USBcontrols[0].get_axis(0))
        self.Throttle = Joystick.valueMap(self,self.USBcontrols[0].get_axis(1)) 
        self.Roll = Joystick.valueMap(self,self.USBcontrols[1].get_axis(0))
        self.Pitch = Joystick.valueMap(self,self.USBcontrols[1].get_axis(1))  
        print(str(self.Yaw) + "," + str(self.Throttle) + "," + str(self.Roll) + "," + str(self.Pitch))

        self.dof4 = [self.Yaw,self.Throttle,self.Roll,self.Pitch]

        return self.dof4

    def buttonsUSB(self):
        self.buttonsA = '000'
        self.buttonsB = '000'
       
        for x in range(self.controllerbuttonNumber[0]):
            if self.USBcontrols[0].get_button(x) == 1:
                self.buttonsA = '0' + str(x+1)
                if x < 9:
                    self.buttonsA = '00' + str(x+1)

        for x in range(self.controllerbuttonNumber[1]):
            if self.USBcontrols[1].get_button(x) == 1:
                self.buttonsB = '0' + str(x+1)
                if x < 9:
                    self.buttonsB = '00' + str(x+1)
        
        self.buttons = [self.buttonsA,self.buttonsB]

        return self.buttons

    def hatUSB(self):
        self.hatA = '0000'
        self.hatB = '0000'
                
        for positionHat in range(self.controllerhatNumber[0]):
            hat = self.USBcontrols[0].get_hat(positionHat)
            if hat[0] == -1:
                self.hatA = '1000'
            elif hat[0] == 1:
                self.hatA = '0100'
            if hat[1] == 1:
                self.hatA = '0010'
            elif hat[1] == -1:
                self.hatA = '0001'
    
        for positionHat in range(self.controllerhatNumber[1]):
            hat = self.USBcontrols[1].get_hat(positionHat)
            if hat[0] == -1:
                self.hatB = '1000'
            elif hat[0] == 1:
                self.hatB = '0100'
            if hat[1] == 1:
                self.hatB = '0010'
            elif hat[1] == -1:
                self.hatB = '0001'
        
        self.hat = [self.hatA,self.hatB]

        return self.hat

