# This is the servo library for the course, adapted from the example file.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

import time
import Adafruit_PCA9685
import signal
import math
from lib import encoders

# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1

DI_WHEEL = 2.61
RD_WHEEL = DI_WHEEL/2
DM_WHEEL = 3.95 #separation
IN_PER_TICK = 0.256
LINEAR_V_MAX = (10*math.pi*RD_WHEEL)/6
R_S_MAX = 0.80 #from slides

measuredRPSright = list(())
measuredRPSleft = list(())

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
# Need to remove this in production most likely.
def ctrlC(signum, frame):
    print("Exiting")

    # Stop the servos
    pwm.set_pwm(LSERVO, 0, 0)
    pwm.set_pwm(RSERVO, 0, 0)

    exit()

#hack to test if floats are equal
def FloatEq (x,y):
    return abs(x-y) < 1e-20

def SatSpeeds0to100(speed):
    if speed > 0:
        return min(speed,100)
    elif speed < 0:
        return max(speed, -100)
    else:
        return 0

def ExecuteCoast(inches): #move forwards some number of inches
    print("Coasting for ", inches, " inches")
    encoders.resetCounts()
    setSpeeds(50,50)
    while(encoders.getCounts()[0] < inches/IN_PER_TICK and encoders.getCounts()[1] < inches/IN_PER_TICK):
        time.sleep(0.01)
    setSpeeds(0,0) #stop
    return 0

def Execute90(dir): #-1 = left, +1 = right
    print("executing 90 degree right turn")
    encoders.resetCounts()
    setSpeeds(dir*50,-dir*50)
    while encoders.getCounts()[0] < 13 and encoders.getCounts()[1] < 13:
        time.sleep(0.01)
    setSpeeds(0,0) #stop
    return 0

#range 1.4-1.6, mapped from 1.5 by scaling factor of 0.001
def setSpeeds(Lspeed,Rspeed):
    Lspeed = SatSpeeds0to100(Lspeed)
    Rspeed = SatSpeeds0to100(Rspeed)
    pwm.set_pwm(LSERVO, 0, math.floor( (1.5+Lspeed*0.001) / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor( (1.5-Rspeed*0.001) / 20 * 4096))

def setSpeedsRPS(rpsLeft,rpsRight):
    setSpeeds(rpsLeft*(100.0/R_S_MAX),rpsRight*(100.0/R_S_MAX))

def setSpeedsIPS(ipsLeft,ipsRight):
    setSpeedsRPS(ipsLeft/(2*math.pi*RD_WHEEL),ipsRight/(2*math.pi*RD_WHEEL))

def setSpeedsVW(v,w):
    if(FloatEq(w,0)):
        #move in a straight line, do not attempt division by zero
        setSpeedsIPS(v,v)
        return 0
    else:
        R = v/w #radius of curve = distance to ICC
        if(w>0):
            setSpeedsIPS(w*(R+DM_WHEEL/2),w*(R-DM_WHEEL/2))
        else:
            setSpeedsIPS(w*(R+DM_WHEEL/2),w*(R-DM_WHEEL/2))
        return 0
def calibrateSpeeds():
    global R_S_MAX
    global measuredRPSright
    global measuredRPSleft

    setSpeeds(0,0)
    encoders.resetCounts()
    setSpeeds(0,100)
    time.sleep(1)

    start = time.monotonic()
    while(start+10>time.monotonic()):
        measuredRPSright.append(encoders.getSpeeds()[1])
        time.sleep(0.03)

    start = time.monotonic()
    setSpeeds(0,0)
    time.sleep(0.03)
    setSpeeds(100,0)

    while(start+10>time.monotonic()):
        measuredRPSleft.append(encoders.getSpeeds()[0])
        time.sleep(0.03)

    start = time.monotonic()
    setSpeeds(0,0)
    time.sleep(0.03)
    setSpeeds(100,100)

    while(start+10>time.monotonic()):
        measuredRPSright.append(encoders.getSpeeds()[1])
        measuredRPSleft.append(encoders.getSpeeds()[0])
        time.sleep(0.03)

    setSpeeds(0,0)

    R_S_MAX = (sum(measuredRPSleft)/len(measuredRPSleft)+sum(measuredRPSright)/len(measuredRPSright))/2





# Attach the Ctrl+C signal interrupt
# Need to remove this in production most likely.
signal.signal(signal.SIGINT, ctrlC)

# Initialize the servo hat library.
# 50Hz is used for the frequency of the servos.
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

# Write an initial value of 1.5, which keeps the servos stopped.
# Due to how servos work, and the design of the Adafruit library,
# the value must be divided by 20 and multiplied by 4096.
pwm.set_pwm(LSERVO, 0, math.floor(1.5 / 20 * 4096))
pwm.set_pwm(RSERVO, 0, math.floor(1.5 / 20 * 4096))