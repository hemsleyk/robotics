import time, math
from lib import servos, ThreadedWebcam, blob, distance

YtCsX = 0.0 #measured x-coordinate of goal in camera space (px)
YtCsY = 480 #measured y-coordinate of goal in camera space (px)
YtCsD = 0.0 #measured diameter of goal (px)
RtCs = 320.00 #desired centerpoint of goal in camera space (px)
deadzoneCs = 50 #deadzone in camera space (px)
YtdF = 5.0 #measured distance to goal in world space (in)
RtWs = 2.5 #desired distance to goal in world space (in)
YtdL = 5.0 #measured distance of left sensor
YtdR = 5.0 #measured distance of right sensor
deadzoneWs = 0.15 #deadzone in world space (in)
satisfiedCsD = 250

def ExecCV():
    global YtdF, YtdL, YtdR, YtCsX, YtCsY, YtCsD
    goalBlobs = blob.DetectPoints(camera) #must be able to see goal from initial point or will never find it?
    YtdF = distance.fSensor.get_distance()/25.4 #convert to inches
    YtdR = distance.rSensor.get_distance()/25.4 #convert to inches
    YtdL = distance.lSensor.get_distance()/25.4 #convert to inches

    if goalBlobs: #goal is visible, execute motion to goal
        YtCsX = goalBlobs[0].pt[0] #store the last known X for proportional control
        YtCsY = goalBlobs[0].pt[1] #store the last known Y for wall vs goal determination
        YtCsD = goalBlobs[0].size

def SeekGoal(): #either rotate to goal or move to goal
    while(True):
        ExecCV()
        if math.fabs(RtCs-YtCsX) > deadzoneCs and YtdF*2.54 > 10 and YtdL*2.54 > 10: #free of any walls
            appliedChange = Kp/4*(RtCs-YtCsX)
            if appliedChange < 0: #need minimum
                appliedChange = min(appliedChange, -10)
            else:
                appliedChange = max(appliedChange, 10)
            servos.setSpeeds(-appliedChange,appliedChange)
            print("centering on goal")
            print("center (px): ", RtCs, "actual (px): ", YtCsX)
            print("height (px): ", YtCsY)
            print("diameter (px): ", YtCsD)
            print("applied delta: ", appliedChange)
            time.sleep(0.02)
        elif (YtdF*2.54 < 10 or YtdL*2.54 < 10) and YtCsY > 100:
            WallFollowing() #allow wall following before goal is obtained
        else:
            while(ExecCV()): #as long as we can see goal
                if math.fabs(RtWs-YtdF) > deadzoneWs and (YtCsY < 100 or YtCsD <= satisfiedCsD): #need to approach
                    if YtdF*2.54 < 12.5 and (YtCsD < satisfiedCsD or YtCsY > 125): #non-goal wall must be in front.
                        WallFollowing()
                    else:
                        appliedChange = -Kp*(RtWs-YtdF)
                        servos.setSpeedsIPS(appliedChange,appliedChange) #correct distance to the goal
                        print("approaching goal")
                        print("Distance (in): ", RtWs, "actual (in): ", YtdF)
                        print("height (px): ", YtCsY)
                        print("diameter (px): ", YtCsD)
                else: #must be at goal
                    print("at the goal")
                    print("Distance (in): ", RtWs, "actual (in): ", YtdF)
                    print("height (px): ", YtCsY) #typical ~200
                    print("diameter (px): ", YtCsD) #typical ~-225
                    servos.setSpeeds(0,0)
                time.sleep(0.02)
    return 1

def WallFollowing():
    print("wall handling")
    while(True):
        ExecCV()
        if(YtdF*2.54 < 12.5): #initial turn or cornered
            global YtCsX
            YtCsX = 0.0 #assume we turned right away from goal
            servos.Execute90(1) #90 degree right turn
        elif(YtdF*2.54 > 20 and YtdL*2.54 > 20): #fell off wall
            servos.ExecuteCoast(5.0) #get some distance
            break  #free to locate goal again.
        #elif (YtCsY < 85 or YtCsD > satisfiedCsD) and (YtdL*2.54 > 20 and YtdF*2.54 > 20):
        #    print ("saw clear path to goal")
        #    break #unobstructed path to goal
        else: #follow the wall
            print("wall following")
            print("V ", -Kp*(10-YtdF*2.54), "W", -Kp*(10-YtdL*2.54)*math.pi/2)
            servos.setSpeedsVW(-Kp*(10-YtdF*2.54),-Kp*(10-YtdL*2.54)*math.pi/2)
        time.sleep(0.02)
    return 0


camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control,"))
if (servos.FloatEq(Kp,0)): exit()

print("Calibrating")
servos.calibrateSpeeds()

SeekGoal()

#time to shut down
camera.stop()