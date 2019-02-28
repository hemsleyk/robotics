import time
from lib import encoders, servos, distance
for count in range(1, 30):
    # Print measurement
    print("Front: {}".format(distance.fSensor.get_distance())) #data read, pipe to file via CLI?
    time.sleep(1) #distance has access to time
