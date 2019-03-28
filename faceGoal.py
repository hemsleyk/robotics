from lib import servos, camera, blob
goalX = 0.0
GoalFound = False
blob.InitCV()

def FrameGoal():
    print("Goal is not visible, seeking.")
    #servos.setSpeeds(50,-50) #set velocity
    return 0

while True:
    goalBlob = blob.DetectPoints()(0)
    while goalBlob: #goal exists
        goalX = goalBlob.x #store the last known X for proportional control
        print(goalBlob.x)
    FrameGoal() #goal isn't visible

#time to shut down
blob.ShutdownCV()