#!/usr/bin/env python3
'''
This file contains a number of values needed for the scripts related to maze simulation.
'''

import numpy as np
from math import pi

# Board dimensions in mm.
FrameSize = np.array([333, 285])
MazeSize = np.array([270, 230])

# Ball characteristics in mm, mm/s, mm/s^2, kg.
BallStartingPosition = np.array([100, 100])
BallStartingVelocity = np.array([0, 0])
BallStartingAcceleration = np.array([0, 0])
BallRadius = 6
BallMass = 0.1

# Artificial drag on ball: approximates air resistance and friction.
Drag = 0.5

# Scaling factor from mm to pixels.
PixelScale = 3

# Tilt angle for manual maze tilt.
ThetaStep = 0.1 * pi

# Colours
Black   = (0  ,   0,   0)
White   = (255, 255, 255)
Blue    = (217, 231, 249)
Grey    = (169, 169, 169)

if __name__ == "__main__":
    import doctest
    doctest.testmod()