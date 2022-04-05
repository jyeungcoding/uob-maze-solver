#!/usr/bin/env python3
"""
This file contains the code we will use to capture frames from the PiCamera. Note that
the video port of the camera was used to improve capture speed. Similarly, it was found
that grabbing the latest frame each time from capture_continous() resulted in higher capture
speeds than running capture() each time. However, the capture delay is still significat,
ranging from 50ms to 110ms. Multithreading in the main code should be considered.
"""

# Import modules.
from picamera.array import PiRGBArray # Allows conversion of frames to cv2 array format.
from picamera import PiCamera
from time import sleep, perf_counter
import cv2
import numpy as np

# Import classes.
from image_detection import ImageProcessor

def main():

	""" PICAMERA INITIALISATION START """
	# Initialise the camera.
	# Set sensor mode to 4. Refer to Raspicam documentation. Size: 1640x1232, framerate: 40fps.
	Camera = PiCamera(sensor_mode = 4) # See if fixing the camera settings improves performance.
	# Camera.framerate = 20 # Can set the camera's framerate.
	# Create an object containing an array in the correct openCV format to store each frame. The camera arg just saves a reference to the camera.
	Capture = PiRGBArray(Camera, size = (640, 480)) # Size should be the same as the size of the input frames.
	sleep(0.2) # Wait for the camera to warm up.
	# Outputs an infinite iterable that inserts the next frame into Capture as the output every time you call it.
	# Change frame format to BGR (for openCV) and resize it to (640, 480) for faster processing. Use video port for faster frame capture.
	Frames = Camera.capture_continuous(Capture, format = "bgr", resize = (640, 480), use_video_port = True)
	""" PICAMERA INITIALISATION END """

	""" IMAGE PROCESSOR INITIALISATION START """
	MazeSize = np.array([275, 230]) # [mm]
	HSVLimitsBlue = np.array([[97, 45, 10], [139, 157, 73]])
	HSVLimitsGreen = np.array([[26, 33, 18], [76, 194, 87]])
	ImageProcessor_ = ImageProcessor(perf_counter(), MazeSize, HSVLimitsBlue, HSVLimitsGreen)
	""" IMAGE PROCESSOR INITIALISATION END """
	while True:

		""" IMAGE CAPTURE START """
		Capture.truncate(0) # Clear Capture so the next frame can be inserted.
		Frame = next(Frames) # If there is a new frame, grab it.
		Image = Frame.array # Store the array from the frame object.
		#Image = Capture.array # The line above is equivalent to this since next(Frames) returns Capture filled with the current frame.
		#cv2.imshow("Image", Image) # Display Image.
		""" IMAGE CAPTURE END """

		""" IMAGE DETECTION START """
		Active, Position = ImageProcessor_.update(perf_counter(), Image) # Find ball position.
		print(Active, Position)
		""" IMAGE DETECTION END """

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	Camera.close() # Don't forget to turn off the camera.
	cv2.destroyAllWindows() # Don't forget to close all windows.

if __name__ == '__main__':
	main()
