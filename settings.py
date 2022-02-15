#!/usr/bin/env python3
'''
This file contains settings required for maze control and simulation.
'''

# Import modules.
import numpy as np
from math import pi

''' PHYSICAL DIMENSIONS '''
# Board dimensions.
FrameSize = np.array([332, 286]) # [mm]
MazeSize = np.array([274.5, 229.5]) # [mm]
FrameHorizontal = (FrameSize[1] - MazeSize[1]) / 2 # [mm]
FrameVertical = (FrameSize[0] - MazeSize[0]) / 2 # [mm]

# Ball dimensions.
BallRadius = 6.335 # [mm]
BallMass = 0.009 # [kg]

# Hole dimensions.
HoleRadius = 7.37 # [mm]

''' SIMULATION SETTINGS '''
# Default ball settings.
Position = np.array([50, 50]) # [mm]
Velocity = np.array([0, 0]) # [mm/s]

# Tilt angle for manual maze tilt.
ThetaStep = 0.01 * pi

# Artificial drag on ball: approximates air resistance and friction.
Drag = 0.6

# Coefficient of reflectivity off walls. Positive floats.
FrameBounce = 0.06
WallBounce = 0.01

''' GRAPHICAL SETTINGS '''
# Scaling factor from mm to pixels.
PixelScale = 2 # PyGame rounds pixels to the nearest ones digit, can cause slight graphical errors.

# Colours
Black   = (0  , 0  , 0  )
White   = (255, 255, 255)
Blue    = (0  , 0  , 255)
Grey    = (169, 169, 169)
DimGrey = (105, 105, 105)
Red     = (255, 0  , 0  )
Purple  = (75 , 0  , 130)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
