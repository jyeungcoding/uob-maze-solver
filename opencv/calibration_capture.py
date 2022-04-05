#!/usr/bin/env python3
"""
This file contains a script for capturing a series of 20 calibration images. The screen
shows a preview of the image to be captured; press c to capture the image.
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

Camera = PiCamera()
print(Camera.resolution)
rawCapture = PiRGBArray(Camera, size=(1024, 768))
time.sleep(0.2)

ImageNumber = 1
while ImageNumber < 21:
	Camera.capture(rawCapture, format="bgr", resize=(1024, 768))
	Image = rawCapture.array
	cv2.imshow("calibration_images/{}.jpg".format(ImageNumber), Image)

	key = cv2.waitKey(1) & 0xFF
	if key == ord("c"):
		cv2.imwrite("calibration/{}.jpg".format(ImageNumber), Image)
		cv2.destroyWindow("calibration_images/{}.jpg".format(ImageNumber))
		ImageNumber += 1

	rawCapture.truncate(0)
	if key == ord("q"):
		break
Camera.close()
cv2.destroyAllWindows()
