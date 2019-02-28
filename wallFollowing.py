import time, math
from lib import encoders, servos, distance

Rt = 5.0

Kp = float(input("Value of Kp for prop. control:"))
if (servos.FloatEq(Kp,0)): exit()
else:
    Dt = time.monotonic() #access time via distance
    while True: #prop control here
        #Yt variables
        YtdF = distance.fSensor.get_distance()/25.4 #convert to inches
        YtdR = distance.rSensor.get_distance()/25.4 #convert to inches
        YtdL = distance.lSensor.get_distance()/25.4 #convert to inches
        if(math.fabs(YtdF-YtdR) < 0.25*Rt):
            servos.setSpeedsVW(Kp*(Rt-YtdF),Kp*(Rt-YtdR)*math.pi/6)
            time.sleep(0.025)
        else:
            servos.setSpeedsVW(-Kp*(Rt-YtdF),-Kp*(Rt-YtdR)*math.pi/6)
            time.sleep(0.025)

        #if (YtdF <= 2*Rt):
	    #getting cornered, WALL NOT SAFE
            #servos.setSpeedsVW(1.25, -math.pi/2)
        #elif (YtdR >= 2*Rt):
		#wall has disappeared completely
            #servos.setSpeedsVW(2.5, math.pi/2)
        #else:
		#follow the safe wall
            #servos.setSpeedsIPS(Rt-Kp*(Rt-YtdR),Rt-Kp*(YtdR-Rt))
            #servos.setSpeedsIPS((-Kp*(Rt-YtdF)),-Kp*(Rt-YtdF-YtdR))
        #print("Distance: {}\tTime: {}".format(YtdF, time.monotonic() - Dt)) #data read, pipe to file?