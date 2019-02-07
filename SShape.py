from lib import encoders, servos
import math
import time

def MoveSShape(R1, R2, Y):
    encoders.resetCounts()
    counts = encoders.getCounts()
    D1 = math.pi*R1
    D2 = math.pi*R2
    D = D1+D2
    V = D/Y

    #portion of task spent on each arc
    P1 = D1/D
    P2 = D2/D

    if(V > servos.LINEAR_V_MAX):
        print("Requested action exceeds theoretical maximum velocity")
        print("Maximum velocity:",servos.LINEAR_V_MAX)
        print("Requested velocity:",V)
        return 1
    else: #stop at ticks*IN_PER_TICK>=inches
        print("Beginning s-shaped motion of",D,"inches over",Y,"seconds with a velocity of",V,"in/s")
        servos.setSpeedsVW(V*P1,P1*2*math.pi*(1/(P1*Y))) #using w=2*pi*f as the formula to find w
        while(counts[0] <= D1/servos.IN_PER_TICK and counts[1] <= D1/servos.IN_PER_TICK): counts = encoders.getCounts()
        
        servos.setSpeeds(0,0) #stop the robot
        time.sleep(0.05) #robot stops fast!
        
        input("Press enter to continue")
        encoders.resetCounts() #clean slate
        counts = encoders.getCounts() #need to do this too
        servos.setSpeedsVW(-V*P2,P2*2*math.pi*(1/(P2*Y)))
        while(counts[0] <= D2/servos.IN_PER_TICK and counts[1] <= D2/servos.IN_PER_TICK): counts = encoders.getCounts()
        servos.setSpeeds(0,0)
        return 0

while True:
    R1 = float(input("R1 in inches, 0 to quit:"))
    if (servos.FloatEq(R1,0)): exit()
    R2 = float(input("R2 in inches, 0 to quit:"))
    if (servos.FloatEq(R2,0)): exit()
    else:
        seconds = float(input("Time in seconds Y to complete maneuver:"))
        if (servos.FloatEq(seconds,0)):
            print("Seconds is a divisor and cannot be zero")
            exit()
        else:
            MoveSShape(R1,R2,seconds)