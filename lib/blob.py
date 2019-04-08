# This program demonstrates advanced usage of the OpenCV library by
# using the SimpleBlobDetector feature along with camera threading.
# The program displays two windows: one for adjusting the mask,
# and one that displays the detected blobs in the (masked) image.
# Adjust the HSV values until blobs are detected from the camera feed.
# There's also a params file in the same folder that can be adjusted.

# Helpful links:
# https://www.learnopencv.com/blob-detection-using-opencv-python-c/
# https://docs.opencv.org/3.4.1/da/d97/tutorial_threshold_inRange.html
# https://docs.opencv.org/3.4.1/d0/d7a/classcv_1_1SimpleBlobDetector.html
# https://docs.opencv.org/3.4.1/d2/d29/classcv_1_1KeyPoint.html
# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/

import cv2 as cv
import time

FPS_SMOOTHING = 0.9

# Default HSV ranges
# Not anymore! Specified for hot pink!
# Note: the range for hue is 0-180, not 0-255
minH =   170; minS = 77; minV = 80
maxH = 180; maxS = 255; maxV = 255

# Initialize the threaded camera
# You can run the unthreaded camera instead by changing the line below.
# Look for any differences in frame rate and latency.
 # UnthreadedWebcam()

params = cv.SimpleBlobDetector_Params()
detector = cv.SimpleBlobDetector_create(params)

# Attempt to open a SimpleBlobDetector parameters file if it exists,
# Otherwise, one will be generated.
# These values WILL need to be adjusted for accurate and fast blob detection.
fs = cv.FileStorage("lib/params.yaml", cv.FILE_STORAGE_READ) #yaml, xml, or json
if fs.isOpened():
    detector.read(fs.root())
else:
    print("WARNING: params file not found! Creating default file.")
    fs2 = cv.FileStorage("params.yaml", cv.FILE_STORAGE_WRITE)
    detector.write(fs2)
    fs2.release()
fs.release()

# Create windows

def DetectPoints(camera):
    # Get a frame
    frame = camera.read()

    # Blob detection works better in the HSV color space
    # (than the RGB color space) so the frame is converted to HSV.
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Create a mask using the given HSV range
    mask = cv.inRange(frame_hsv, (minH, minS, minV), (maxH, maxS, maxV))

    # Run the SimpleBlobDetector on the mask.
    # The results are stored in a vector of 'KeyPoint' objects,
    # which describe the location and size of the blobs.
    keypoints = detector.detect(mask)

    #return largest
    return sorted(keypoints, key=lambda keypoint: keypoint.response,reverse=True)