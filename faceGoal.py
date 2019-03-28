from lib import servos, camera, blob
goalX = 0.0
GoalFound = False
def FrameGoal():
    print("Goal is not visible, seeking.")
    #servos.setSpeeds(50,-50) #set velocity
    return 0

while True:
    detectedBlobs = sorted(blob.keypoints, key=lambda keypoint: keypoint.response,reverse=True)
    while GoalFound: #center the goal, stay stationary, use propcon
        print("wee")
    FrameGoal() #goal isn't visible