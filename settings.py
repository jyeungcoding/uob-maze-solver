#!/usr/bin/env python3
'''
This file contains settings required for maze control and simulation.
'''

# Import modules.
import numpy as np
from math import pi
import pygame

''' PHYSICAL DIMENSIONS '''
# Board dimensions.
FrameSize = np.array([332, 286]) # [mm]
MazeSize = np.array([275, 230]) # [mm]
FrameHorizontal = (FrameSize[1] - MazeSize[1]) / 2 # [mm]
FrameVertical = (FrameSize[0] - MazeSize[0]) / 2 # [mm]

# Ball dimensions.
BallRadius = 6.335 # [mm]
BallMass = 0.009 # [kg]

# Hole dimensions.
HoleRadius = 7.37 # [mm]

''' IMAGE DETECTION SETTINGS '''

# Upper and lower HSV limits for the blue ball.
HSVLimitsBlue = np.array([[70, 58, 0], [120, 201, 75]])

# Upper and lower HSV limits for the green frame.
HSVLimitsGreen = np.array([[22, 95, 23], [86, 248, 148]])

''' CONTROL SETTINGS '''
# Maximum frequency of the control loop.
ControlFrequency = 15 # [Hz]

# Maximum frequency of the graphics loop.
GraphicsFrequency = 4 # [Hz]

# Maximum frequency of whole loop.
MaxFrequency = 50 # [Hz]

# PID Coefficients
Kp = 3.4e-4
Ki = 3e-4
Kd = 3e-4

# Maximum proportional term allowed.
PMax = 0.032

# Static boost coefficient.
Ks = 0.01

# Static boost length coefficient. Higher numbers produce a shorter static boost.
Kst = 2

# Number of error values to buffer for PID derivative calculation.
BufferSize = 3

# Minimum tilt angle allowed.
MinTheta = np.array([0, 0])

# Maximum motor angle.
SaturationLimit = np.array([pi / 3.5, pi / 3.5])

# Tolerance distance for calibration.
CalibrationTolerance = 2 # [mm]

# Time before calibrated.
CalibrationTime = 2.5 # [s]

# How close the ball has to be to each checkpoint.
CheckpointRadius = 8 # [mm]

# Time the ball has to stay within the set point to "pass" it.
SetPointTime = 0

''' SIMULATION SETTINGS '''
# Tilt angle for manual maze tilt.
ThetaStep = 0.01 * pi

# Artificial drag on ball: approximates air resistance and friction.
Drag = 10

# Coefficient of reflectivity off walls. Positive floats0
FrameBounce = 0.06
WallBounce = 0.01

# Simulated +- error value from image detection.
ImageNoise = 1 # [mm]

''' GRAPHICAL SETTINGS '''
# GUI display scaling factor. Use 1 for pi touchscreen.
DisplayScale = 1

# Maze to GUI scaling factor. Don't change.
GUIScale = 1.5 * DisplayScale

# Maze shift for GUI display.
HeaderShift = np.array([0, 51]) * DisplayScale

# Colours
Black      = (0  , 0  , 0  )
White      = (255, 255, 255)
Blue       = (0  , 0  , 255)
Grey       = (169, 169, 169)
DimGrey    = (105, 105, 105)
Red        = (255, 0  , 0  )
Purple     = (75 , 0  , 130)
LightGreen = (80 , 255, 80 )
LightRed   = (255, 100 , 100 )

# Checkpoint Colours
CheckpointColours = {
"SetPoint" : Red,
"Checkpoint" : Blue,
"EndPoint" : Purple
}

# Initialise text module.
pygame.font.init()
# Create fonts.
HeaderFont = pygame.font.SysFont("Times New Roman", 30) # Scaling handled internally.
TextFont = pygame.font.SysFont("Times New Roman", round(19 * DisplayScale))
ButtonFont = pygame.font.SysFont("Times New Roman", 22) # Scaling handled internally.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
