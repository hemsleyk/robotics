import time, math
from lib import servos, ThreadedWebcam, blob, distance

YtCsX = 0.0 #measured x-coordinate of goal in camera space (px)
YtCsY = 480 #measured y-coordinate of goal in camera space (px)
RtCs = 320.00 #desired centerpoint of goal in camera space (px)
deadzoneCs = 30 #deadzone in camera space (px)
YtdF = 5.0 #measured distance to goal in world space (in)
RtWs = 2.5 #desired distance to goal in world space (in)
YtdL = 5.0 #measured distance of left sensor
YtdR = 5.0 #measured distance of right sensor
deadzoneWs = 0.1 #deadzone in world space (in)

def ExecCV():
    global YtdF, YtdL, YtdR, YtCsX, YtCsY
    goalBlobs = blob.DetectPoints(camera) #must be able to see goal from initial point or will never find it?
    YtdF = distance.fSensor.get_distance()/25.4 #convert to inches
    YtdR = distance.rSensor.get_distance()/25.4 #convert to inches
    YtdL = distance.lSensor.get_distance()/25.4 #convert to inches
    
    if goalBlobs: #goal is visible, execute motion to goal
        YtCsX = goalBlobs[0].pt[0] #store the last known X for proportional control
        YtCsY = goalBlobs[0].pt[1] #store the last known Y for wall vs goal determination
        return goalBlobs

def SeekGoal(): #either rotate to goal or move to goal
    while(True):
        ExecCV()
        if math.fabs(RtCs-YtCsX) > deadzoneCs and YtdF*2.54 > 10 and YtdL*2.54 > 10: #free of any walls
            servos.setSpeeds(-Kp/3*(RtCs-YtCsX),Kp/3*(RtCs-YtCsX)) #rotate in place to acquire the goal
            print("centering on goal")
            print("center (px): ", RtCs, "actual (px): ", YtCsX)
            print("height (px): ", YtCsY)
            time.sleep(0.025)
        elif (YtdF*2.54 < 10 or YtdL*2.54 < 10) and YtCsY > 300:
            WallFollowing() #allow wall following before goal is obtained
        else:
            while(ExecCV()): #as long as we can see goal
                if math.fabs(RtWs-YtdF) > deadzoneWs and YtCsY < 90: #need to approach
                    servos.setSpeedsIPS(-Kp*(RtWs-YtdF),-Kp*(RtWs-YtdF)) #correct distance to the goal
                    print("approaching goal")
                    print("Distance (in): ", RtWs, "actual (in): ", YtdF)
                    print("height (px): ", YtCsY)
                elif YtdF*2.54 < 10 and YtCsY >= 90: #non-goal wall detected in front.
                    WallFollowing()
                else: #must be at goal
                    servos.setSpeeds(0,0)
            time.sleep(0.025)
    return 0

def WallFollowing():
    print("wall following")
    while(True):
        ExecCV()
        if(math.fabs(YtdF-YtdL) < 0.5): #in a corner
            servos.Execute90(1) #90 degree right turn
        elif(YtdF*2.54 > 15 ):
            servos.ExecuteCoast(5.0)
            break #left the wall
        elif(YtCsY < 90): break #unobstructed path to goal
        else: #follow the wall
            servos.setSpeedsVW(-Kp*(10-YtdF*2.54),-Kp*(10-YtdL*2.54)*math.pi/6)
        time.sleep(0.05)
    

camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control,"))
if (servos.FloatEq(Kp,0)): exit()

print("Calibrating")
servos.calibrateSpeeds()

SeekGoal()

#time to shut down
camera.stop()