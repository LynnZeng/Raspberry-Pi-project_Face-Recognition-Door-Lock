import pygame
import os
import time
import sys
from pygame.locals import *
import RPi.GPIO as GPIO

import config
import capture_positives
import classify
import passcode
import servo
import client
#import visitor

os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)
   
pygame.init()
pygame.mouse.set_visible(False)
WHITE=255,255,255
circle = 255,0,125
background = 100,100,200
size=width,height=320,240
screen=pygame.display.set_mode(size)


my_font=pygame.font.Font(None,30)
my_buttons1={'Recognize Face':(80,80),'Enter Passcode':(80,160)}
lock_button = {'LOCK':(280,120)}
my_buttons2={'Unlock':(160,40),'Reset Passcode':(160,120),'Return':(160,200)}

info_font=pygame.font.Font(None,30)
info1={'Enter passcode, end with #':(160,120)}
info2={'Passcode does not match':(160,100),'please try again':(160,120)}
info3 = {'Maximum failed passcode':(160,100),' attempts in restriction':(160,120),'Please try again':(160,140),'after 5 minutes':(160,160)}

reset_info = {'Enter new passcode, end with #':(160,120)}
recog_info = {'Could not recognize':(160,100),'please try again':(160,120)}
denied_info =  {'Entrance not allowed by owner':(160,120)}
locked_info = {'The door is locked':(160,120)}
unlocked_info = {'The door is unlocked':(160,120)}
passcode.init()
    
model,model1 = classify.load_data()
sleep_time = 3

count = 0
level ="main"
#steps of passcode info
step =1
#Passcode matched?
matched = False
locked = True
while True:
    if(not GPIO.input(22)):
        exit(0)
    time.sleep(0.1)
    
    #pygame.draw.circle(screen,circle,(280,120),40)
    #for my_text,text_pos in my_buttons1.items():
        #text_surface=my_font.render(my_text,True,WHITE)
        #rect=text_surface.get_rect(center=text_pos)
        #screen.blit(text_surface,rect)
    
    #for my_text,text_pos in lock_button.items():
        #text_surface=my_font.render(my_text,True,WHITE)
        #rect=text_surface.get_rect(center=text_pos)
        #screen.blit(text_surface,rect)
    #pygame.display.flip()

    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos=pygame.mouse.get_pos()
        if(event.type is MOUSEBUTTONUP):
            pos=pygame.mouse.get_pos()
            x,y=pos
            #functions of main level
            if (not matched):
	            if x < 240:
	                if y < 120:
	                    print "Recognize Face button is pressed"
	                    '''TO DO'''
	                    recognized = classify.classify(model,model1)
	
	                    if recognized:
			        #print"Unlock!"
                                confirmation = client.send()
                                print"Remote confirmation"
                                print confirmation
                                if confirmation == "Yes":
                                    if locked == True:
                                        print "Unlock"
	                                servo.unlock()
                                        locked = False
                        
                                    print"The door is unlocked"
                                    level = "unlocked"
                                else:
                                    level = "denied"
                                    print"Entrance not allowed"
	                        #'''Remote Confirmation'''
	                        #'''Servo control'''
	                    else:
                                print"Recognize agian!"
				level = "recogAgain"
	
	
	
	
	
	                else:
	                    print "Enter Passcode button is pressed"
	                    '''To DO'''
	                    '''Passcode part'''
	                    level = "passcode"
	                    
	
	                #else:
                            #print"Visitor buttons is pressed"
                            #if visitor.capture()== "Yes":
                                #if locked == True:
                                    #print "Unlock"
                                    #servo.unlock()
                                    #locked = False

                                #print"The door is unlocked"
                                #level = "unlocked"
                            #else:
                                #level = "denied"
                                #print"Entrance not allowed"
	
	            ###For debugging purpose, delete later       
	            else:
                        print"Lock button is pressed"
                        if not locked:
                            servo.lock()
                            locked = True
                        else:
                            print"The door is already locked"
                            
                        level = "locked"
	                #exit(0)  
	                
	        #functions of second level
	    else:
                if x > 80 and x < 240:
		        
	            if y < 80:
	                '''TODO Servo Control'''
			print"Unlock the door"
                        if locked == True:
                            #print "Unlock"
                            servo.unlock()
                            locked = False

                        print"The door is unlocked"
                        level = "unlocked"
                        count = 0
                        step = 1
                        matched = False
	            elif y < 160:
			print "Reset Passcode"
			level = "reset"
	            else:
			print "Return button is pressed"
			level = "main"
			count = 0
			step =1
			matched = False
		
    screen.fill((background))
    #screen.fill((0,0,0))  
    if level == "main":
        pygame.draw.circle(screen,circle,(280,120),40)
        for my_text,text_pos in lock_button.items():
            text_surface=my_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)     
        for my_text,text_pos in my_buttons1.items():
            text_surface=my_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        
    elif level == "second":	
        for my_text,text_pos in my_buttons2.items():
            text_surface=my_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        
    elif level == "reset":
	for my_text,text_pos in reset_info.items():
            text_surface=info_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        passcode.reset()
        level = "second"

    elif level == "recogAgain":
        print "recogAgain level"
	for my_text,text_pos in recog_info.items():
            text_surface=info_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        time.sleep(sleep_time)
        level = "main"
    elif level == "denied":
        for my_text,text_pos in denied_info.items():
            text_surface=info_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        time.sleep(sleep_time)
        level = "main"
    elif level == "locked":
        for my_text,text_pos in locked_info.items():
            text_surface=info_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        time.sleep(sleep_time)
        level = "main"
    elif level == "unlocked":
        for my_text,text_pos in unlocked_info.items():
            text_surface=info_font.render(my_text,True,WHITE)
            rect=text_surface.get_rect(center=text_pos)
            screen.blit(text_surface,rect)
        pygame.display.flip()
        time.sleep(sleep_time)
        level = "main"


    elif level == "passcode":
        print"passcode level"
        if step == 1:
           
            for my_text,text_pos in info1.items():
                text_surface=info_font.render(my_text,True,WHITE)
                rect=text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
            pygame.display.flip()
            #screen.fill((0,0,0))
            if not passcode.check_passcd():
                count += 1
                if count >= config.PASSCODE_UPLIMIT:
                    step = 3
                else:
                    step = 2
            else:
                print"Passcode is correct"
                matched = True
                level = "second"
        elif step == 2:
            
            for my_text,text_pos in info2.items():
                text_surface=info_font.render(my_text,True,WHITE)
                rect=text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
                    

            pygame.display.flip()
            time.sleep(sleep_time)
            level = "main"
            step =1
        else:
            
            for my_text,text_pos in info3.items():
                text_surface=info_font.render(my_text,True,WHITE)
                rect=text_surface.get_rect(center=text_pos)
                screen.blit(text_surface,rect)
                    

            pygame.display.flip()
            time.sleep(config.break_time)
            level = "main"
            step =1
            count = 0
         
            

                        
                        
