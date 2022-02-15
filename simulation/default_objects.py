#!/usr/bin/env python3
'''
This file generates default objects for maze simulation.
'''

# Import modules.
import numpy as np
import pygame
import math

# Import classes, functions and values.
from objects import Ball, Checkpoint, Maze
from settings import Position, Velocity

# Default ball settings.
DefaultBall = Ball(
    Position, # [mm]
    Velocity, # [mm/s]
)

# Default maze setting.
DefaultMaze = Maze(DefaultBall, [], [], [])

# Generate checkpoints in a circle
Circle = []
Theta = 0
while Theta < 2 * math.pi:
    Circle.append(Checkpoint(np.array([166 + 50 * math.sin(Theta), 143 + 50 * math.cos(Theta)])))
    Theta += math.pi / 8

if __name__ == "__main__":
    import doctest
    doctest.testmod()
