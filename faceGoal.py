import time
from lib import servos, ThreadedWebcam, blob

Yt = 0.0
Rt = 320.00 #desired centerpoint of goal in camera space

def InitCV():
# Initialize the SimpleBlobDetector
    camera.start()
def SatSpeeds0to100(speed):
    if speed > 0:
        return min(speed,100)
    elif speed < 0:
        return max(speed, -100)
    else:
        return 0


camera = ThreadedWebcam.ThreadedWebcam()
camera.start()

Kp = float(input("Value of Kp for prop. control:"))
if (servos.FloatEq(Kp,0)): exit()

while True:
    goalBlobs = blob.DetectPoints(camera)
    if goalBlobs: #goal is visible, so update the x coordinate
        Yt = goalBlobs[0].pt[0] #store the last known X for proportional control
        print("center: ", Rt, "actual: ", Yt)
        print("applied: ", SatSpeeds0to100(Kp*(Rt-Yt)))
    servos.setSpeeds(SatSpeeds0to100(Kp*(Rt-Yt)),SatSpeeds0to100(-Kp*(Rt-Yt))) #rotate in place to center goal
    time.sleep(0.1) #don't constantly hit OpenCV

#time to shut down
camera.stop()