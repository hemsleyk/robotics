from lib import encoders, servos

def MoveForward(inches, seconds):
    encoders.resetCounts()
    counts = encoders.getCounts()
    ips = inches/seconds
    if(ips > servos.LINEAR_V_MAX):
        print("Requested action exceeds theoretical maximum velocity")
        print("Maximum linear velocity:",servos.LINEAR_V_MAX)
        print("Requested linear velocity:",ips)
        return 1
    else: #stop at ticks*IN_PER_TICK>=inches
        print("Beginning forwards motion of",inches,"over",seconds,"seconds with a velocity of",ips,"in/s")
        servos.setSpeedsIPS(ips,ips) #set velocity
        while(counts[0] <= inches/servos.IN_PER_TICK or counts[1] <= inches/servos.IN_PER_TICK): counts = encoders.getCounts()
        servos.setSpeeds(0,0)
        return 0

while True:
    inches = float(input("Distance to move in inches, 0 to quit:"))
    if (inches is 0.0): exit()
    else:
        
        seconds = float(input("Time in seconds to complete maneuver:"))
        if (seconds is 0.0):
            print("Seconds is a divisor and cannot be zero")
            exit()
        else:
            MoveForward(inches,seconds)