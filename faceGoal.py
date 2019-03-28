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
    goalX = goalBlob.x
    while GoalFound: #center the goal, stay stationary, use propcon
        print("wee")
    FrameGoal() #goal isn't visible
blob.ShutdownCV()