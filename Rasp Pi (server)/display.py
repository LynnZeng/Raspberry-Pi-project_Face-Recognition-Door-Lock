import pygame
import os
import time
import sys
from pygame.locals import *

def display():
    os.putenv('SDL_FBDEV','/dev/fb1')
    os.putenv('SDL_VIDEODRIVER','fbcon')
    os.putenv('SDL_MOUSEDRV','TSLIB')
    os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
    pygame.init()
    pygame.mouse.set_visible(False)
    WHITE=255,255,255
    size=width,height=320,240
    screen=pygame.display.set_mode(size)

    
    image = pygame.image.load("/home/pi/project/received_file")
    image = pygame.transform.scale(image,(240,200))
    my_font=pygame.font.Font(None,20)
    my_buttons={'Entrance allowed?':(120,220),'Yes':(280,120),'No':(280,200)}
    while True:
        for event in pygame.event.get():
            if(event.type is MOUSEBUTTONDOWN):
                pos=pygame.mouse.get_pos()
            if(event.type is MOUSEBUTTONUP):
                pos=pygame.mouse.get_pos()
                x,y=pos
                if x > 240:
	            if y> 160:
	                print"Entrance not allowed"
	                screen.fill((0,0,0))
                        pygame.display.update()
	                return "No"
	            else:
	                print"Entrance allowed"
	                screen.fill((0,0,0))
                        pygame.display.update()
	                return "Yes"
                else:
                    exit(0)
        screen.fill((0,0,0))
        for my_text,text_pos in my_buttons.items():
            text_surface=my_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)

        screen.blit(image,(0,0))
        pygame.display.flip()
