import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Matrix = [[1,2,3],[4,5,6],[7,8,9],['*',0,'#']]

Row = [18,23,24,25]
Col = [5,6,13]

for j in range(3):
    GPIO.setup(Col[j],GPIO.OUT)
    GPIO.output(Col[j],1)

for i in range(4):
    GPIO.setup(Row[i],GPIO.IN,pull_up_down = GPIO.PUD_UP)

try:
    while True:
        time.sleep(0.2)
        for j in range(3):
            GPIO.output(Col[j],0)
            for i in range(4):
                if (not GPIO.input(Row[i])):
                    print Matrix[i][j]
                    while(not GPIO.input(Row[i])):
                        pass
            GPIO.output(Col[j],1)
except KeyboardInterrupt:
    GPIO.cleanup()
