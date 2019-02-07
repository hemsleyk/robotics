from lib import encoders, servos
import math

def MoveSShape(R1, R2, Y):
    encoders.resetCounts()
    counts = encoders.getCounts()
    v = math.pi*(R1+R2)/Y
    if(v > servos.LINEAR_V_MAX):
        print("Requested action exceeds theoretical maximum velocity")
        print("Maximum velocity:",servos.LINEAR_V_MAX)
        print("Requested velocity:",v)
        return 1
    else: #stop at ticks*IN_PER_TICK>=inches
        print("Beginning s-shaped motion of",inches,"over",seconds,"seconds with a velocity of",v,"in/s")
        servos.setSpeedsVW(v,v/R1) #set velocity
        while(counts[0] <= inches/servos.IN_PER_TICK or counts[1] <= inches/servos.IN_PER_TICK): counts = encoders.getCounts()
        servos.setSpeeds(v,-v/R2)
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