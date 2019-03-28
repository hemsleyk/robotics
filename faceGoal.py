from lib import servos, ThreadedWebcam, blob
goalX = 0.0
GoalFound = False

def InitCV():
# Initialize the SimpleBlobDetector
    camera.start()

camera = ThreadedWebcam.ThreadedWebcam()
camera.start()
def FrameGoal():
    print("Goal is not visible, seeking.")
    #servos.setSpeeds(50,-50) #set velocity
    return 0

while True:
    goalBlobs = blob.DetectPoints(camera)
    while goalBlobs: #goal exists
        goalX = goalBlobs[0].x #store the last known X for proportional control
        print(goalBlobs[0].pt.x)
    FrameGoal() #goal isn't visible

#time to shut down
camera.stop()