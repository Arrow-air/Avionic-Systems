import pygame
import os
import sys
import multiprocessing

def run_pygame_on_display(display_number, width, height):
    # Set the DISPLAY environment variable for the specific display
    os.environ['DISPLAY'] = f':0.{display_number}'

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f'Pygame on Display {display_number}')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # Define the width and height for the displays
    width, height = 640, 480

    # Create processes for each display
    process1 = multiprocessing.Process(target=run_pygame_on_display, args=(0, width, height))
    process2 = multiprocessing.Process(target=run_pygame_on_display, args=(1, width, height))

    # Start the processes
    process1.start()
    process2.start()

    # Wait for the processes to finish
    process1.join()
    process2.join()
