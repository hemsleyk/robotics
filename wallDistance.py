import time
from lib import encoders, servos, distance

Rt = 5.00 #desired distance in inches

Kp = float(input("Value of Kp for prop. control:"))
if (servos.FloatEq(Kp,0)): exit()
else:
    Dt = time.monotonic() #access time via distance
    while True: #prop control here
        Yt = distance.fSensor.get_distance()/25.4 #convert to inches
        servos.setSpeedsIPS((-Kp*(Rt-Yt)),-Kp*(Rt-Yt))
        print("Distance: {}\tTime: {}".format(Yt, time.monotonic() - Dt)) #data read, pipe to file?
        time.sleep(0.01)