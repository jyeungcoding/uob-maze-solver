#!/usr/bin/env python3
"""
Note from this demo: capturing each frame using the image port creates too much of
a delay. Use the video port and capture_continuous() instead.
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera(sensor_mode=3)
# It seems that the camera arg doesn't actually do anything, just saves a reference to the camera.
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
while True:
	camera.capture(rawCapture, format="bgr", resize=(640, 480))
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = rawCapture.array
	# show the frame
	cv2.imshow("Frame", image)
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	key = cv2.waitKey(50) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
