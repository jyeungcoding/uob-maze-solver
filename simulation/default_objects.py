#!/usr/bin/env python3
'''
This file generates default objects for maze simulation.
'''

# Import modules.
import numpy as np
import pygame

# Import classes, functions and values.
from objects import Ball, Wall, Maze
from settings import Position, Velocity, Acceleration, FrameSize, MazeSize, FrameHorizontal, FrameVertical

# Default ball settings.
DefaultBall = Ball(
    Position, # [mm]
    Velocity, # [mm/s]
    Acceleration # [mm/s^2]
)

# Frame settings.
Frame = [
    Wall(
        np.array([0, 0]), # Standard units (see settings).
        np.array([FrameVertical, FrameSize[1]]) # Standard units (see settings).
    ),
    Wall(
        np.array([FrameSize[0] - FrameVertical, 0]),
        np.array([FrameVertical, FrameSize[1]])
    ),
    Wall(
        np.array([0, 0]),
        np.array([FrameSize[0], FrameHorizontal])
    ),
    Wall(
        np.array([0, FrameSize[1] - FrameHorizontal]),
        np.array([FrameSize[0], FrameHorizontal])
    )
]

# Default maze setting.
DefaultMaze = Maze(FrameSize, DefaultBall, [], [], [])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
