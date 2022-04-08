#!/usr/bin/env python3
"""
This file contains a script for selecting the upper and lower HSV values required
to mask out undesired areas in a picture.
"""

# Import modules.
from tkinter import *
from tkinter import ttk
import cv2
import numpy as np

''' HSV Starting Limits '''
HSVLimits = np.array([[70, 58, 0], [120, 201, 75]])
''' HSV Starting Limits '''

def value_changed(a):
	# This function updates the value labels.
	HMinValueLabel.config(text = HMin.get())
	HMaxValueLabel.config(text = HMax.get())
	SMinValueLabel.config(text = SMin.get())
	SMaxValueLabel.config(text = SMax.get())
	VMinValueLabel.config(text = VMin.get())
	VMaxValueLabel.config(text = VMax.get())


def generate_mask():
	# This function generates the mask and resulting image based on the chosen HVS limits.
	Lower = np.array([HMin.get(), SMin.get(), VMin.get()]) # Lower limits for each HSV value
	Upper = np.array([HMax.get(), SMax.get(), VMax.get()]) # Upper limits

	Mask = cv2.inRange(ImageHSV, Lower, Upper) # Use lower and upper limits to create a mask
	ImageResult = cv2.bitwise_and(Image, Image, mask = Mask) # Use mask to create a new image with only the wanted areas.
	RGBMask = cv2.cvtColor(Mask, cv2.COLOR_GRAY2BGR) # Convert mask to BGR format.
	ImageDisplay = np.hstack((RGBMask, ImageResult)) # Stack images togather

	cv2.imshow("Display", ImageDisplay) # Display result.
	Root.after(50, generate_mask) # Run fucntion recursively.

""" Main Code Start """
# Initialise GUI.
Root = Tk()
Root.geometry("700x160")
Root.title("HSV Limit Calibration")

# Load image.
Path = "111.jpg" # Change this to the filename required.
Image = cv2.imread(Path) # Load image.
ImageHSV = cv2.cvtColor(Image, cv2.COLOR_BGR2HSV) # Convert image to HSV format.

# Initialise limit values.
HMin = IntVar(Root, HSVLimits[0][0])
HMax = IntVar(Root, HSVLimits[1][0])
SMin = IntVar(Root, HSVLimits[0][1])
SMax = IntVar(Root, HSVLimits[1][1])
VMin = IntVar(Root, HSVLimits[0][2])
VMax = IntVar(Root, HSVLimits[1][2])

# Create Slider Labels
HMinLabel = ttk.Label(Root, text = 'Hue Min:')
HMaxLabel = ttk.Label(Root, text = 'Hue Max:')
SMinLabel = ttk.Label(Root, text = 'Saturation Min:')
SMaxLabel = ttk.Label(Root, text = 'Saturation Max:')
VMinLabel = ttk.Label(Root, text = 'Value Min:')
VMaxLabel = ttk.Label(Root, text = 'Value Max:')
# Position Slider Labels
HMinLabel.grid(column = 0, row = 0)
HMaxLabel.grid(column = 0, row = 1)
SMinLabel.grid(column = 0, row = 2)
SMaxLabel.grid(column = 0, row = 3)
VMinLabel.grid(column = 0, row = 4)
VMaxLabel.grid(column = 0, row = 5)

# Create Sliders
HMinSlider = ttk.Scale(Root, from_ = 0, to = 179, length = 500, orient = HORIZONTAL, variable = HMin, command = value_changed)
HMaxSlider = ttk.Scale(Root, from_ = 0, to = 179, length = 500, orient = HORIZONTAL, variable = HMax, command = value_changed)
SMinSlider = ttk.Scale(Root, from_ = 0, to = 255, length = 500, orient = HORIZONTAL, variable = SMin, command = value_changed)
SMaxSlider = ttk.Scale(Root, from_ = 0, to = 255, length = 500, orient = HORIZONTAL, variable = SMax, command = value_changed)
VMinSlider = ttk.Scale(Root, from_ = 0, to = 255, length = 500, orient = HORIZONTAL, variable = VMin, command = value_changed)
VMaxSlider = ttk.Scale(Root, from_ = 0, to = 255, length = 500, orient = HORIZONTAL, variable = VMax, command = value_changed)
# Position Sliders
HMinSlider.grid(column = 1, row = 0)
HMaxSlider.grid(column = 1, row = 1)
SMinSlider.grid(column = 1, row = 2)
SMaxSlider.grid(column = 1, row = 3)
VMinSlider.grid(column = 1, row = 4)
VMaxSlider.grid(column = 1, row = 5)

# Create Value Labels
HMinValueLabel = ttk.Label(Root, text = HMin.get())
HMaxValueLabel = ttk.Label(Root, text = HMax.get())
SMinValueLabel = ttk.Label(Root, text = SMin.get())
SMaxValueLabel = ttk.Label(Root, text = SMax.get())
VMinValueLabel = ttk.Label(Root, text = VMin.get())
VMaxValueLabel = ttk.Label(Root, text = VMax.get())
# Position Value Labels
HMinValueLabel.grid(column = 2, row = 0)
HMaxValueLabel.grid(column = 2, row = 1)
SMinValueLabel.grid(column = 2, row = 2)
SMaxValueLabel.grid(column = 2, row = 3)
VMinValueLabel.grid(column = 2, row = 4)
VMaxValueLabel.grid(column = 2, row = 5)

Root.after(50, generate_mask) # Run mask generation function.
Root.mainloop()
""" Main Code End """
