
class Joystick:
    
    def __init__(self,joystick,time) -> None:
        self.old_min = -1
        self.old_max = 1
        self.new_min = 100
        self.new_max = 355
        
        self.joystick = joystick
        self.time = time
        self.clock = self.time.Clock()  
        
        self.USBJoystick = self.joystick.get_init()
        self.CANJoystick = JoystickCAN.isPresent(self)

        self.packet = [bytes('', 'ascii')]

        if self.USBJoystick == True:
            self.USBcontrols = [self.joystick.Joystick(id) for id in range(self.joystick.get_count())]      # call the joystick controls
            [i.init() for i in self.USBcontrols]                            # initialise the USB controls
            self.controllerName = [str(i.get_name()) for i in self.USBcontrols]
            self.controlleraxesNumber = [i.get_numaxes() for i in self.USBcontrols]
            self.controllerhatNumber = [i.get_numhats() for i in self.USBcontrols]
            self.controllerbuttonNumber = [i.get_numbuttons() for i in self.USBcontrols]

            print('Joystick No: ' + str(len(self.controllerName)))
            print(self.controllerName)
        
        
        
        if self.CANJoystick == True:
            self.CANcontrols = ''
            self.controllerName = ''
            self.controlleraxesNumber = ''
            self.controllerhatNumber = ''
            self.controllerbuttonNumber = ''
        

    def valueMap(self,old_value):
        new_value = str(int(round(( ( old_value - self.old_min ) / (self.old_max - self.old_min) ) * (self.new_max - self.new_min) + self.new_min)))
        return(new_value)

class JoystickUSB(Joystick):

    def __init__(self, joystick, time) -> None:
        super().__init__(joystick, time)

    def packetStruct(self):
        self.packet = self.dof4ControlUSB() + self.buttonsUSB() + self.hatUSB()
        return self.packet
    
    def dof4ControlUSB(self):
        self.Yaw = bytes(self.valueMap(self.USBcontrols[0].get_axis(0)), 'ascii')
        self.Throttle = bytes(self.valueMap(self.USBcontrols[0].get_axis(1)), 'ascii')
        self.Roll = bytes(self.valueMap(self.USBcontrols[1].get_axis(0)), 'ascii')
        self.Pitch = bytes(self.valueMap(self.USBcontrols[1].get_axis(1)), 'ascii') 
        #print(str(self.Yaw) + "," + str(self.Throttle) + "," + str(self.Roll) + "," + str(self.Pitch))

        self.dof4 = [self.Yaw,self.Throttle,self.Roll,self.Pitch]
        #self.clock.tick(1000)
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
        
        self.buttons = [bytes(self.buttonsA, 'ascii'),bytes(self.buttonsB, 'ascii')]
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
        
        self.hat = [bytes(self.hatA, 'ascii'),bytes(self.hatB, 'ascii')]
        return self.hat
    
    def run(self):
        self.clock.tick(100)

class JoystickCAN(Joystick):

    def __init__(self, joystick, time) -> None:
        super().__init__(joystick, time) 

    def packetStruct(self):
        return self.packet

    def DOF4ControlCAN(self):
         pass
    
    def buttonsCAN(self):
         pass
    
    def hatCAN(self):
         pass
    
    def isPresent(self):
        self.Present = False
        return self.Present
    
    def run(self):
        self.clock.tick(1000)

