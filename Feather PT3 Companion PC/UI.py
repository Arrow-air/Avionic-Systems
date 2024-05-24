from pygame import image, draw, font
import os

class UI:

    def __init__(self,display,time,modeselect) -> None:
        
        self.modeselect = modeselect
        self.mode = {0:'GCS',1:'FUI'}
        
        self.display = display
        self.time = time
        self.mode = {0:'GCS',1:'FUI'}
        

        if self.modeselect == self.mode.get(0):
            self.screen = self.display.set_mode((1860,1020),display=1)
            print(self.modeselect)
        elif self.modeselect == self.mode.get(1):
            self.screen = self.display.set_mode((1280,800),display=1)
            print(self.modeselect)

        self.display.set_caption('UI Windows 2X Middle Split')
        self.display.set_icon(image.load('images/feather-icon.png'))
        self.screen.fill("blue")

        self.clock = self.time.Clock() 

        print('Display No: ' + str(self.display.get_num_displays()))
        print('Display Size: ' + str(self.display.get_window_size()))

        print("UI Init")

    def uiUpdate(self,packet):
        self.packet = packet
        self.background()
        self.stateUpdate(self.packet)
        self.infoUpdate(self.packet)
        self.run(self.packet)

    def background(self):
        self.screen.fill("blue")
        draw.line(self.screen,(200,200,200,0.1),(self.screen.get_width()/2,50),(self.screen.get_width()/2,950),2)

    def run(self,packet):
        self.packet = packet
        self.display.flip()
        self.clock.tick(100)

    def stateUpdate(self,packet):
        self.packet = packet
        self.text = font.Font(None,20).render(str(self.packet),True,(200,200,150))
        self.screen.blit(self.text,(10,50))

    def infoUpdate(self,packet):
        self.packet = packet
        self.text = font.Font(None,20).render(str(self.packet),True,(200,200,150))
        self.screen.blit(self.text,(960,50))
    
    def textDisplay(self):
        pass
