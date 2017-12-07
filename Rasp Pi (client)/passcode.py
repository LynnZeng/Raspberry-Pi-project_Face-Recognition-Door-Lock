''' 4-digit passcode'''
import RPi.GPIO as GPIO
import time
import pygame
import os

import config

#star_list=[]
pos=[(100,160),(140,160),(180,160),(220,160)]

Matrix = [['1','2','3'],['4','5','6'],['7','8','9'],['*','0','#']]

Row = [18,23,24,21]
Col = [5,6,13]


def show_digit(star_list):
    #os.putenv('SDL_FBDEV','/dev/fb1')
    #os.putenv('SDL_VIDEODRIVER','fbcon')
    #os.putenv('SDL_MOUSEDRV','TSLIB')
    #os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
    
    #pygame.init()
    #pygame.mouse.set_visible(False)
    WHITE=255,255,255
    size=width,height=320,240
    background = 100,100,200
    screen=pygame.display.set_mode(size)

    my_font=pygame.font.Font(None,30)
    info1={'Enter passcode, end with #':(160,120)}
  
    info2=zip(pos,star_list)
    #print(info2)
    info2_dict=dict(info2)
    #print(info2_dict)
    start = time.time()
    end = time.time()
    while end - start < 0.5:

        for my_text,text_pos in info1.items():
            text_surface=my_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        for text_pos,my_text in info2_dict.items():
            text_surface=my_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()

        screen.fill(background)
        end = time.time()

def check_passcd():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for j in range(3):
        GPIO.setup(Col[j],GPIO.OUT)
        GPIO.output(Col[j],1)
    for i in range(4):
        GPIO.setup(Row[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)
    enter = []
    star_list = []
    while True:
        time.sleep(0.2)
        for j in range(3):
            GPIO.output(Col[j],0)
            for i in range(4):
                if (not GPIO.input(Row[i])):
                    if (Matrix[i][j] != '#'):
                        enter.append(Matrix[i][j])
                        if len(star_list) == 0:
                            star_list.append(Matrix[i][j])
                        else:
                            star_list[len(star_list)-1] = '*'
                            star_list.append(Matrix[i][j])
                        print(star_list)
                        show_digit(star_list)
                    else:
                        print "enter"
                        print(enter)
                        passcode = config.reset()
                        print "passcode"
                        print(passcode)
                        print"Passcode matched?"
                        print(enter == passcode)
                        return(enter == passcode)

                    while(not GPIO.input(Row[i])):
                        pass

            GPIO.output(Col[j],1)

    return False
#return(enter == config.PASSCODE)

def init():
    init_passcd = [1,2,3,4]
    file = open(config.PASSCODE_FILE,'w')
    file.writelines(["%s\n" % digit for digit in init_passcd])
    file.close()
    
def reset():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for j in range(3):
        GPIO.setup(Col[j],GPIO.OUT)
        GPIO.output(Col[j],1)
    for i in range(4):
        GPIO.setup(Row[i],GPIO.IN,pull_up_down = GPIO.PUD_UP) 
    new_passcd = []
    star_list = []

    while True:
        time.sleep(0.2)
        for j in range(3):
            GPIO.output(Col[j],0)
            for i in range(4):
                if (not GPIO.input(Row[i])):
                    if (Matrix[i][j] != '#'):
                        new_passcd.append(Matrix[i][j])
                        if len(star_list) == 0:
                            star_list.append(Matrix[i][j])
                        else:
                            star_list[len(star_list)-1] = '*'
                            star_list.append(Matrix[i][j])
                        show_digit(star_list)
                    else:
                        #print(enter)
                        print"New Passcode"
                        print(new_passcd)
                        file = open(config.PASSCODE_FILE,'w')
                        file.writelines(["%s\n" % digit for digit in new_passcd])
                        file.close()
                        #print(config.PASSCODE)
                        return                   

                    while(not GPIO.input(Row[i])):
                        pass

            GPIO.output(Col[j],1)
