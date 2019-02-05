import lib

def MoveForward(inches, seconds):
    counts = lib.getCounts()
    #stop at ticks*IN_PER_TICK>=inches
    SetSpeeds(100,100)
    while(counts[0] >= inches*IN_PER_TICK or counts[1] >= inches*IN_PER_TICK): counts = lib.getCounts()
    SetSpeeds(0,0)

MoveForward(12, 999999)

            