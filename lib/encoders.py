# This program demonstrates usage of the digital encoders.
# After executing the program, manually spin the wheels and observe the output.
# See https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/ for more details.

import time
import RPi.GPIO as GPIO
import signal
from lib import distance

# Pins that the encoders are connected to
LENCODER = 17
RENCODER = 18

#left, right encoders respectively
lCount = 0
lTime = 0
lSpeed = 0
rCount = 0
rTime = 0
rSpeed = 0


#clean slate
def resetCounts():
    global lCount
    lCount = 0
    global rCount
    rCount = 0
    print("Left encoder reset to ", getCounts()[0])
    print("Right encoder reset to ", getCounts()[1])

#return as tuple (immutable)
def getCounts():
    lCount
    rCount
    #print("L:",lCount)
    #print("R:",rCount)
    return lCount,rCount


# This function is called when the left encoder detects a rising edge signal.
def onLeftEncode(pin):
    #print("Left encoder ticked!")
    global lCount
    global lTime
    global lSpeed
    lCount+=1

    #track the speed
    now = time.monotonic()
    lSpeed = (1.0 / 32.0) / (now-lTime)
    lTime=now

# This function is called when the right encoder detects a rising edge signal.
def onRightEncode(pin):
    #print("Right encoder ticked!")
    global rCount
    global rTime
    global rSpeed
    rCount+=1
    
    #track the speed
    now = time.monotonic()
    rSpeed = (1.0 / 32.0) / (now-rTime)
    rTime=now


# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
def ctrlC(signum, frame):
    print("Exiting")
    GPIO.cleanup()
    distance.lSensor.stop_ranging()
    distance.fSensor.stop_ranging()
    distance.rSensor.stop_ranging()
    exit()

def getSpeeds():
    global lSpeed
    global rSpeed
    return lSpeed,rSpeed

# Attach the Ctrl+C signal interrupt
signal.signal(signal.SIGINT, ctrlC)
    
# Set the pin numbering scheme to the numbering shown on the robot itself.
GPIO.setmode(GPIO.BCM)

# Set encoder pins as input
# Also enable pull-up resistors on the encoder pins
# This ensures a clean 0V and 3.3V is always outputted from the encoders.
GPIO.setup(LENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RENCODER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Attach a rising edge interrupt to the encoder pins
GPIO.add_event_detect(LENCODER, GPIO.RISING, onLeftEncode)
GPIO.add_event_detect(RENCODER, GPIO.RISING, onRightEncode)

# Prevent the program from exiting by adding a looping delay.
#while True:
#    time.sleep(1)
#    getCounts()

