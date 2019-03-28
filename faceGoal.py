import time
from lib import servos, ThreadedWebcam, blob

Yt = goalX = 0.0
Rt = 250.00 #desired centerpoint of goal in camera space

def InitCV():
# Initialize the SimpleBlobDetector
    camera.start()

camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control:"))
if (servos.FloatEq(Kp,0)): exit()

while True:
    goalBlobs = blob.DetectPoints(camera)
    if goalBlobs: #goal is visible, so update the x coordinate
        goalX = goalBlobs[0].pt[0] #store the last known X for proportional control
        print(goalBlobs[0].pt[0])
    servos.setSpeedsIPS((Kp*(Rt-Yt)),-Kp*(Rt-Yt)) #rotate in place to center goal
    time.sleep(0.1) #don't constantly hit OpenCV

#time to shut down
camera.stop()