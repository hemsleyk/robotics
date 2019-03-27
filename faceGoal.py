from lib import servos, camera, blob

def FrameGoal():
    print("Goal is not visible, seeking.")
    servos.setSpeeds(50,-50) #set velocity
    return 0

while True:
    GoalFound = False
    while GoalFound: #center the goal, stay stationary, use propcon
    FrameGoal()