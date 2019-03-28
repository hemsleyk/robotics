import time
from lib import servos, ThreadedWebcam, blob, distance

YtCs = 0.0 #measured x-coordinate of goal in camera space (px)
RtCs = 320.00 #desired centerpoint of goal in camera space (px)
YtWs = 5.0 #measured distance to goal in world space (inches), set to 5 initially ...
RtWs = 5.0 #desired distance to goal in world space (inches)

def InitCV():
# Initialize the SimpleBlobDetector
    camera.start()

camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control,"))
if (servos.FloatEq(Kp,0)): exit()

while True:
    goalBlobs = blob.DetectPoints(camera)
    if goalBlobs: #goal is visible, so update the x coordinate
        YtCs = goalBlobs[0].pt[0] #store the last known X for proportional control
        if RtCs-YtCs < 75:
            YtWs = distance.fSensor.get_distance()/25.4 #only measure if we think we are angled towards goal
        else:
            YtWs = 5.0 #disable motion to goal
        print("center (px): ", RtCs, "actual (px): ", YtCs)
        print("applied: ", (Kp/2*(RtCs-YtCs)))
    servos.setSpeeds(-Kp/2*(RtCs-YtCs)-Kp*(RtWs-YtWs),Kp/2*(RtCs-YtCs)-Kp*(RtWs-YtWs)) #rotate + move to center goal
    time.sleep(0.025) #don't constantly hit OpenCV

#time to shut down
camera.stop()