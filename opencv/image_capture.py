#!/usr/bin/env python3
"""
Note: for lowest capture time, use video port and capture_continuous(). This reduces
frame capture time to bellow 100ms.
"""

# Import modules.
from picamera.array import PiRGBArray # Allows conversion of frames to cv2 array format.
from picamera import PiCamera
from time import sleep
import cv2

# Import classes, functions and settins.

""" PICAMERA INITIALISATION START """
# Initialise the camera.
# Set sensor mode to 4. Refer to Raspicam documentation. Size: 1640x1232.
# Sets the framerate at which video-port based image captures will run.
Camera = PiCamera(sensor_mode = 4) # See if fixing the camera settings improves performance.
# Camera.framerate = 20 # Can set the camera's framerate.
# Create an object containing an array in the correct openCV format to store each frame. The camera arg just saves a reference to the camera.
Capture = PiRGBArray(Camera, size = (640, 480)) # Size should be the same as the size of the input frames.
sleep(0.2) # Wait for the camera to warm up.
# Outputs an infinite iterable that inserts the next frame into Capture as the output every time you call it.
# Change frame format to BGR (for openCV) and resize it to (640, 480) for faster processing. Use video port for faster frame capture.
Frames = Camera.capture_continuous(Capture, format = "bgr", resize = (640, 480), use_video_port = True)
""" PICAMERA INITIALISATION END """

while True:

	""" IMAGE CAPTURE START """
	Frame = next(Frames) # If there is a new frame, grab it.
	Image = Frame.array # Store the array from the frame object.
	#Image = Capture.array # The line above is equivalent to this since next(Frames) returns Capture filled with the current frame.
	Capture.truncate(0) # Clear Capture so the next frame can be inserted.
	cv2.imshow("Frame", Image)
	""" IMAGE CAPTURE END """

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

Camera.close()
