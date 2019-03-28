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
    goalBlob = blob.DetectPoints(camera)(0)
    while goalBlob: #goal exists
        goalX = goalBlob.x #store the last known X for proportional control
        print(goalBlob.x)
    FrameGoal() #goal isn't visible

#time to shut down
camera.stop()