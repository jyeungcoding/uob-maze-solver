#!/usr/bin/env python3

# Import modules.
import cv2
import numpy as np

Image = cv2.imread("2.png")

ImageBlurred = cv2.GaussianBlur(Image, (11, 11), 0) # Blur image to remove high frequency noise.
ImageHSV = cv2.cvtColor(ImageBlurred, cv2.COLOR_BGR2HSV) # Convert image to HSV format.
HSVLimitsBlue = np.array([h_min, s_min, v_min], [h_max, s_max, v_max])
Mask = cv2.inRange(ImageHSV, HSVLimitsGreen[0], HSVLimitsGreen[1]) # Use lower and upper limits to create a mask
Mask2 = cv2.erode(Mask, None, iterations=2)
Mask3 = cv2.dilate(maMasksk, None, iterations=2)
ImageCanny = cv2.Canny(Mask3, 50, 50) # Detect lines in the image.

Img1 = np.hstack((ImageBlurred, ImageHSV, ImageHSV, ImageHSV))
Img2 = np.hstack((Mask, Mask2, Mask3, ImageCanny))
Img3 = np.vstack((Img1, Img2))

cv2.imshow("All", Img3)

cv2.waitKey(0)
