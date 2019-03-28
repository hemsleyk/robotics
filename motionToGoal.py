import time, math
from lib import servos, ThreadedWebcam, blob, distance

YtCs = 0.0 #measured x-coordinate of goal in camera space (px)
RtCs = 320.00 #desired centerpoint of goal in camera space (px)
deadzoneCs = 20 #deadzone in camera space (px)
YtWs = 0.0 #measured distance to goal in world space (in)
RtWs = 5.0 #desired distance to goal in world space (in)
deadzoneWs = 0.1 #deadzone in world space (in)

def InitCV():
# Initialize the SimpleBlobDetector
    camera.start()

camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control,"))
if (servos.FloatEq(Kp,0)): exit()

while True:
    goalBlobs = blob.DetectPoints(camera)
    YtWs = distance.fSensor.get_distance()/25.4 #measure front sensor

    if goalBlobs: #goal is visible, so update the x coordinate
        YtCs = goalBlobs[0].pt[0] #store the last known X for proportional control
    if math.fabs(RtCs-YtCs) > deadzoneCs:
        servos.setSpeeds(-Kp/3*(RtCs-YtCs),Kp/3*(RtCs-YtCs)) #rotate in place to acquire the goal
        print("seeking goal")
        print("center (px): ", RtCs, "actual (px): ", YtCs)
    elif math.fabs(RtWs-YtWs) > deadzoneWs:
        servos.setSpeedsIPS(-Kp*(RtWs-YtWs),-Kp*(RtWs-YtWs)) #correct distance to the goal
        print("approaching goal")
        print("Distance (in): ", RtWs, "actual (in): ", YtWs)
    else: #nowhere to go
        servos.setSpeeds(0,0)
    time.sleep(0.05) #don't constantly hit OpenCV

#time to shut down
camera.stop()