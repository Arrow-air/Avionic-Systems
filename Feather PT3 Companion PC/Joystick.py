import j1939

class Joystick:
    
    def __init__(self,joystick,time,modeselect) -> None:

        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}

        self.dataDictionary = {'command_pitch':0,'command_roll':0,'command_yaw':0,'command_throttle':0,'switch_states':0}

        self.old_min = -1
        self.old_max = 1
        self.new_min = -1
        self.new_max = 1
        
        self.joystick = joystick
        self.time = time
        self.clock = self.time.Clock()  
        
        self.USBJoystick = self.joystick.get_init()
        self.CANJoystick = JoystickCAN.isPresent(self)

        self.packet = {}

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
            
        print("Joystick Init")

    def valueMap(self,old_value):
        #new_value = str(int(round(( ( old_value - self.old_min ) / (self.old_max - self.old_min) ) * (self.new_max - self.new_min) + self.new_min)))
        new_value = str(( ( old_value - self.old_min ) / (self.old_max - self.old_min) ) * (self.new_max - self.new_min) + self.new_min)
        return(new_value)

class JoystickUSB(Joystick):

    def __init__(self, joystick, time,modeselect) -> None:
        super().__init__(joystick, time, modeselect)

    def packetStruct(self):
        self.dataDictionary['command_pitch'] = self.dof4ControlUSB()[0]# + self.buttonsUSB() + self.hatUSB()
        self.dataDictionary['command_roll'] = self.dof4ControlUSB()[1]# + self.buttonsUSB() + self.hatUSB()
        self.dataDictionary['command_yaw'] = self.dof4ControlUSB()[2]# + self.buttonsUSB() + self.hatUSB()
        self.dataDictionary['command_throttle'] = self.dof4ControlUSB()[3]# + self.buttonsUSB() + self.hatUSB()
        self.dataDictionary['switch_states'] = (self.buttonsUSB()[0] + self.buttonsUSB()[1])

        self.packet = self.dataDictionary
        return self.packet
    
    def dof4ControlUSB(self):
        self.Yaw = self.valueMap(self.USBcontrols[0].get_axis(0))
        self.Throttle = self.valueMap(self.USBcontrols[0].get_axis(1))
        self.Roll = self.valueMap(self.USBcontrols[1].get_axis(0))
        self.Pitch = self.valueMap(self.USBcontrols[1].get_axis(1)) 
        #print(str(self.Yaw) + "," + str(self.Throttle) + "," + str(self.Roll) + "," + str(self.Pitch))

        self.dof4 = [self.Pitch,self.Roll,self.Yaw,self.Throttle]
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
    
    def run(self):
        self.clock.tick(100)

class JoystickCAN(Joystick):

    def __init__(self, joystick, time, modeselect) -> None:
        super().__init__(joystick, time, modeselect) 

        self.bus = j1939.Bus(interface='can1')
        self.node = j1939.Node(name=0x12345, bus=self.bus)

        # Add some callbacks for message handling
        self.node.add_handler(self.joystick1_callback, pgn=0x00FDD6)
        self.node.add_handler(self.joystick2_callback, pgn=0x00FDD8)

        self.joystick_data = {
            "joystick_1": {"x": None, "y": None, "buttons": []},
            "joystick_2": {"x": None, "y": None, "buttons": []}
        }

        self.packet = {}

        self.start()

    def packetStruct(self):
        
        self.read_joysticks()

        self.dataDictionary['command_pitch'] = self.joystick_data["joystick_2"]["y"]
        self.dataDictionary['command_roll'] = self.joystick_data["joystick_2"]["y"]
        self.dataDictionary['command_yaw'] = self.joystick_data["joystick_1"]["x"]
        self.dataDictionary['command_throttle'] = self.joystick_data["joystick_1"]["x"]
        self.dataDictionary['switch_states'] = (self.joystick_data["joystick_1"]["buttons"]).join(',') + (self.joystick_data["joystick_2"]["buttons"]).join(',')

        self.packet = self.dataDictionary
        return self.packet
    
    def isPresent(self):

        self.read_joysticks()
        
        if (self.joystick_data["joystick_2"]["y"] == None ) or (self.joystick_data["joystick_1"]["y"] == None):
            self.Present = False
        else:
            self.Present = True

        return self.Present
    
    def start(self):
        self.bus.start()

    def stop(self):
        self.bus.stop()

    def joystick1_callback(self, pgn, priority, source_address, data):
        self.joystick_data["joystick_1"]["x"] = int.from_bytes(data[0:2], byteorder='little', signed=True)
        self.joystick_data["joystick_1"]["y"] = int.from_bytes(data[2:4], byteorder='little', signed=True)
        self.joystick_data["joystick_1"]["buttons"] = [bool(data[4] & (1 << i)) for i in range(8)]

    def joystick2_callback(self, pgn, priority, source_address, data):
        self.joystick_data["joystick_2"]["x"] = int.from_bytes(data[0:2], byteorder='little', signed=True)
        self.joystick_data["joystick_2"]["y"] = int.from_bytes(data[2:4], byteorder='little', signed=True)
        self.joystick_data["joystick_2"]["buttons"] = [bool(data[4] & (1 << i)) for i in range(8)]

    def read_joysticks(self):
        return self.joystick_data

