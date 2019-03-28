import time, math
from lib import servos, ThreadedWebcam, blob, distance

YtCs = 0.0 #measured x-coordinate of goal in camera space (px)
RtCs = 320.00 #desired centerpoint of goal in camera space (px)
deadzoneCs = 30 #deadzone in camera space (px)
YtdF = 0.0 #measured distance to goal in world space (in)
RtWs = 5.0 #desired distance to goal in world space (in)
deadzoneWs = 0.1 #deadzone in world space (in)
wallFollowing = False

def InitCV():
# Initialize the SimpleBlobDetector
    camera.start()

camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control,"))
if (servos.FloatEq(Kp,0)): exit()

while True:
    goalBlobs = blob.DetectPoints(camera) #must be able to see goal from initial point or will never find it?
    YtdF = distance.fSensor.get_distance()/25.4 #convert to inches
    YtdR = distance.rSensor.get_distance()/25.4 #convert to inches
    YtdL = distance.lSensor.get_distance()/25.4 #convert to inches
    if goalBlobs:
        YtCs = goalBlobs[0].pt[0] #store the last known X for proportional control
    
    if goalBlobs and YtdF*2.54 > 10 and wallFollowing is False: #goal is visible, execute motion to goal
        print("motion to goal")
        if math.fabs(RtCs-YtCs) > deadzoneCs:
            servos.setSpeeds(-Kp/3*(RtCs-YtCs),Kp/3*(RtCs-YtCs)) #rotate in place to acquire the goal
            print("seeking goal")
            print("center (px): ", RtCs, "actual (px): ", YtCs)
        elif math.fabs(RtWs-YtdF) > deadzoneWs:
            servos.setSpeedsIPS(-Kp*(RtWs-YtdF),-Kp*(RtWs-YtdF)) #correct distance to the goal
            print("approaching goal")
            print("Distance (in): ", RtWs, "actual (in): ", YtdF)
        else: #nowhere to go
            servos.setSpeeds(0,0)
    elif YtdF*2.54 < 10 or wallFollowing is True: #cast dist to cm, execute wall following
        wallFollowing = True #left turn robot
        print("wall following")
        if(YtdL*2.54 > 15 and YtdF > 15): #safety margin
            wallFollowing = False
        elif(math.fabs(YtdF-YtdL) < 0.5): #in a corner
            servos.Execute90(1) #90 degree right turn
        else: #follow
            servos.setSpeedsVW(-Kp*(4-YtdF),-Kp*(4-YtdL)*math.pi/6)
    elif math.fabs(RtCs-YtCs) > deadzoneCs: #goal is not visible and we are not at an obstacle
        print("finding goal")
        servos.setSpeeds(-Kp/3*(RtCs-YtdF),Kp/3*(RtCs-YtCs)) #rotate in place to acquire the goal
    else:
        #enter dead (stuck) state
        print("x-x")
        servos.setSpeeds(0,0)
    time.sleep(0.05) #don't constantly hit OpenCV

#time to shut down
camera.stop()