import time, math
from lib import servos, ThreadedWebcam, blob

Yt = 0.0
Rt = 320.00 #desired centerpoint of goal in camera space
deadzone = 30 #deadzone of goal center in pixels

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
        Yt = goalBlobs[0].pt[0] #store the last known X for proportional control
        print("center (px): ", Rt, "actual (px): ", Yt)
        print("applied: ", (Kp/2*(Rt-Yt)))
    if math.fabs(Rt-Yt) > deadzone:
        servos.setSpeeds(-Kp/3*(Rt-Yt),Kp/3*(Rt-Yt)) #rotate in place to center goal
    else:
        servos.setSpeeds(0,0)
    
    time.sleep(0.025) #don't constantly hit OpenCV

#time to shut down
camera.stop()