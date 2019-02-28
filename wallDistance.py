from lib import encoders, servos, distance
desiredDistance = 5.00
while True:
    Kp = float(input("Value of Kp for prop. control:"))
    if (servos.FloatEq(Kp,0)): exit()
    else:
        exit() #prop control here