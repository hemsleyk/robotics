from lib import encoders, servos, distance
for count in range(1, 30):
#    # Get a measurement from each sensor
    lDistance = distance.lSensor.get_distance()
    fDistance = distance.fSensor.get_distance()
    rDistance = distance.rSensor.get_distance()
    
    # Print each measurement
    print("Left: {}\tFront: {}\tRight: {}".format(lDistance, fDistance, rDistance)) #data read, pipe to file?
    distance.time.sleep(1) #distance has access to time
