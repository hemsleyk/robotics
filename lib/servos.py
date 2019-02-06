# This is the servo library for the course, adapted from the example file.
# See https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/ for more details.

import time
import Adafruit_PCA9685
import signal
import math

# The servo hat uses its own numbering scheme within the Adafruit library.
# 0 represents the first servo, 1 for the second, and so on.
LSERVO = 0
RSERVO = 1

DI_WHEEL = 2.61
RD_WHEEL = DI_WHEEL/2
IN_PER_TICK = 0.256
LINEAR_V_MAX = (10*math.pi*RD_WHEEL)/6
R_S_MAX = 0.83 #from datasheet

# This function is called when Ctrl+C is pressed.
# It's intended for properly exiting the program.
# Need to remove this in production most likely.
def ctrlC(signum, frame):
    print("Exiting")
    
    # Stop the servos
    pwm.set_pwm(LSERVO, 0, 0);
    pwm.set_pwm(RSERVO, 0, 0);
    
    exit()

#range 1.4-1.6, mapped from 1.5 by scaling factor of 0.001
def setSpeeds(Lspeed=0.0,Rspeed=0.0):
    pwm.set_pwm(LSERVO, 0, math.floor( (1.5+Lspeed*0.001) / 20 * 4096))
    pwm.set_pwm(RSERVO, 0, math.floor( (1.5-Rspeed*0.001) / 20 * 4096))

#def setSpeedsRPS(rpsLeft,rpsRight):
    #pwm.set_pwm(LSERVO, 0, math.floor(rpsLeft/20*4096))
def setSpeedsRPS(rpsLeft,rpsRight):
    setSpeeds(rpsLeft*(100/R_S_MAX),rpsRight(100/R_S_MAX))

def setSpeedsIPS(ipsLeft,ipsRight):
    setSpeeds(ipsLeft*(100/LINEAR_V_MAX),ipsRight*(100/LINEAR_V_MAX))

def setSpeedsVW(v,w):
    if(w is 0):
        print("w must not be zero!")
        return 1
    else:
        float R = v/w; //radius of curve = distance to ICC
        setSpeedsIPS(w*(R+3.95/2),w*(R-3.95/2))
        return 0
    
}

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