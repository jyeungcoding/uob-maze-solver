#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera(sensor_mode=4)
#camera.framerate=20 # Sets the framerate at which video-port based image captures will run.
# It seems that the camera arg doesn't actually do anything, just saves a reference to the camera.
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.2)
# capture frames from the camera
frames = camera.capture_continuous(rawCapture, format="bgr", resize=(640, 480), use_video_port=True) # Creates an inerable of frames.
while True:
	try:
		LastTime = time.perf_counter()
		frame = next(frames)
		TimeStep = time.perf_counter() - LastTime
		print(TimeStep * 1000)
		# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		#image = frame.array
		#cv2.imshow("Frame", image) # show the frame
		key = cv2.waitKey(1) & 0xFF
		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)
		# if the `q` key was pressed, break from the loop
		time.sleep(0.1)
		if key == ord("q"):
			break
	except StopIteration:
		break
