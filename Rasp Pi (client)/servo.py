import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)


def unlock():
    pulse=1.7
    pause=20
    p=GPIO.PWM(17,1000/(pulse+20))
    #start PWM, pulse=1.5ms, pause=20ms
    dc=pulse*100/(pulse+pause)
    
    p.start(dc)
    time.sleep(0.4)
    p.stop()
    #raw_input("Press enter to stop")
    #GPIO.cleanup()
    #exit(0)

def lock():
    pulse=1.3
    pause=20
    p=GPIO.PWM(17,1000/(pulse+20))
    #start PWM, pulse=1.5ms, pause=20ms
    dc=pulse*100/(pulse+pause)

    p.start(dc)
    time.sleep(0.4)
    p.stop()
    #raw_input("Press enter to stop")
    #GPIO.cleanup()
    #exit(0)
