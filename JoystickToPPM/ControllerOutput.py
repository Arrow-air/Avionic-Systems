#!/usr/bin/env python

import sys
import time
import pygame
import serial

pygame.init()                               # initiaise pygame
controls = [pygame.joystick.Joystick(0), pygame.joystick.Joystick(1)]      # call the joystic controls
clock = pygame.time.Clock()                 # intialise pygame refresh and call it clock
controls[0].init()                             # initialise the controls
controls[1].init()                             # initialise the controls


#arduino =  serial.Serial('/dev/ttyUSB0', 9600,timeout = 1) # connect to the arduino's serial port
#time.sleep(2)

arduino =  serial.Serial('COM4', 9600,timeout = 1)  # connect to the arduino's serial port
time.sleep(2)

EXIT = False

old_min = -1
old_max = 1
new_min = 100
new_max = 355

def valueMap(old_value):
    new_value = str(int(round(( ( old_value - old_min ) / (old_max - old_min) ) * (new_max - new_min) + new_min)))
    return(new_value)
    
while not EXIT:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXIT = True
    
    controller1Name = str(controls[0].get_name())
    controller1axesNumber = controls[0].get_numaxes()
    controller1hatNumber = controls[0].get_numhats()
    controller1buttonNumber = controls[0].get_numbuttons()

    controller2Name = str(controls[1].get_name())
    controller2axesNumber = controls[1].get_numaxes()
    controller2hatNumber = controls[1].get_numhats()
    controller2buttonNumber = controls[1].get_numbuttons()

    Yaw = valueMap(controls[0].get_axis(0))
    Throttle = valueMap(controls[0].get_axis(1)) 

    Roll = valueMap(controls[1].get_axis(0))
    Pitch = valueMap(controls[1].get_axis(1))  
    print(str(Yaw) + "," + str(Throttle) + "," + str(Roll) + "," + str(Pitch))

    
    c = '000'
    d = '0000'
    e = '000'
    f = '0000'

    for x in range(controller1buttonNumber):
        if controls[0].get_button(x) == 1:
            c = '0' + str(x+1)
            if x < 9:
                c = '00' + str(x+1)
                
    for positionHat in range(controller1hatNumber):
        hat = controls[0].get_hat(positionHat)
        if hat[0] == -1:
            d = '1000'
        elif hat[0] == 1:
            d = '0100'
        if hat[1] == 1:
            d = '0010'
        elif hat[1] == -1:
            d = '0001'
    
    for x in range(controller2buttonNumber):
        if controls[1].get_button(x) == 1:
            e = '0' + str(x+1)
            if x < 9:
                e = '00' + str(x+1)
                
    for positionHat in range(controller2hatNumber):
        hat = controls[1].get_hat(positionHat)
        if hat[0] == -1:
            f = '1000'
        elif hat[0] == 1:
            f = '0100'
        if hat[1] == 1:
            f = '0010'
        elif hat[1] == -1:
            f = '0001'
            
    control = ['<' + Throttle,Pitch,Roll,Yaw,c,e + '>']         # save strings in a list
    cstring = ",".join(control)                 # convert list to a single string with commas seperating values
                
    print(cstring)
    arduino.write(bytes(cstring, 'ascii'))                      # print string to shell and write data to arduino with a 0.1ms delay
    time.sleep(0.0001)
    
    if  controls[1].get_button(1) == 1:
        pygame.quit()                           # This is used to quit pygame and use any internal program within the python
        quit()

    clock.tick(1000)

pygame.quit()
quit()
