from multiprocessing import Process
import time
import pygame,os,time,sys

def a():
    
    pygame.init()

    lcd1 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,display=0)
    lcd1.fill(pygame.Color('black'))
    pygame.draw.line(lcd1,pygame.Color('red'),(0,0),(1920,1080),1)

    pygame.display.update()
    time.sleep(4)
    pygame.quit()
    
def b():
    pygame.init()
        
    lcd2 = pygame.display.set_mode((0, 0), pygame.FULLSCREEN,display=1)
    lcd2.fill(pygame.Color('black'))
    pygame.draw.line(lcd2,pygame.Color('blue'),(0,0),(1920,1080),1)

    pygame.display.update()
    time.sleep(4)
    pygame.quit()
    
if __name__ == '__main__':
    
    pa = Process(target=a)
    pa.start()
    
    pb = Process(target=b)
    pb.start()
    
    pa.join()
    pb.join()
    
    print('end')