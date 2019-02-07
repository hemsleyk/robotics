from lib import encoders, servos
import math
import time

def MoveSShape(R1, R2, Y):
    encoders.resetCounts()
    counts = encoders.getCounts()
    D1 = math.pi*R1
    D2 = math.pi*R2
    D = D1+D2
    v = D/Y
    Y1 = Y*R1/D
    Y2 = Y*R2/D

    if(v > servos.LINEAR_V_MAX):
        print("Requested action exceeds theoretical maximum velocity")
        print("Maximum velocity:",servos.LINEAR_V_MAX)
        print("Requested velocity:",v)
        return 1
    else: #stop at ticks*IN_PER_TICK>=inches
        print("Beginning s-shaped motion of",D,"inches over",Y,"seconds with a velocity of",v,"in/s")
        #servos.setSpeedsVW(v/(D1/D),4*((v/R1)/(D1/D))) #set velocity
        servos.setSpeedsVW(v,2*v/R1)
        while(counts[0] <= D1/servos.IN_PER_TICK and counts[1] <= D1/servos.IN_PER_TICK): counts = encoders.getCounts()
        servos.setSpeeds(0,0)
        time.sleep(0.1)
        input("Press enter to continue")
        encoders.resetCounts()
        counts = encoders.getCounts()
        #servos.setSpeedsVW(v/(D2/D),-2*((v/R2)/(D2/D)))
        servos.setSpeedsVW(v,2*v/R2)
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