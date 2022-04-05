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
rawCapture = PiRGBArray(Camera, size=(640, 480))
time.sleep(0.2)

ImageNumber = 1
while ImageNumber < 21:
	Camera.capture(rawCapture, format="bgr", resize=(640, 480))
	Image = rawCapture.array
	cv2.imshow("calibration/{0:s}.jpg".format(ImageNumber), Image)

	if key == ord("c"):
		cv2.imwrite(("calibration/{0:s}.jpg".format(ImageNumber), Image)
		ImageNumber += 1

	rawCapture.truncate(0)
	time.wait(0.1)
	if key == ord("q"):
		break
