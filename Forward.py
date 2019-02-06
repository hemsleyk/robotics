from lib import encoders, servos

def MoveForward(inches=0.0, seconds=0.0):
    encoders.resetCounts()
    counts = encoders.getCounts()
    if(inches/seconds > servos.LINEAR_V_MAX):
        print("Requested action exceeds theoretical maximum velocity")
        print("Maximum linear velocity:",servos.LINEAR_V_MAX)
        print("Requested linear velocity:",inches/seconds)
        return 1
    else: #stop at ticks*IN_PER_TICK>=inches
        servos.setSpeedsIPS(inches/seconds,inches/seconds) #set velocity
        while(counts[0] <= inches/servos.IN_PER_TICK or counts[1] <= inches/servos.IN_PER_TICK): counts = encoders.getCounts()
        servos.setSpeeds(0,0)
        return 0

MoveForward(12, 5)
#MoveForward(12,5)
#MoveForward(12,5/3)