from lib import encoders, servos

def MoveForward(inches, seconds):
    counts = encoders.getCounts()
    #stop at ticks*IN_PER_TICK>=inches
    servos.setSpeeds(100,100)
    while(counts[0] <= inches*servos.IN_PER_TICK or counts[1] <= inches*servos.IN_PER_TICK): counts = encoders.getCounts()
    servos.setSpeeds(0,0)

MoveForward(12, 999999)

            