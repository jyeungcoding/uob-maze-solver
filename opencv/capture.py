#!/usr/bin/env python3

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

camera = PiCamera(sensor_mode=4, resolution = (1024, 768))
camera.framerate=20
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.2)

camera.capture(rawCapture, format="bgr", resize=(640, 480), use_video_port=True)
image = rawCapture.array
cv2.imwrite("111.jpg", image)