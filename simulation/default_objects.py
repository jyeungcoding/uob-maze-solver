#!/usr/bin/env python3
'''
This file generates default objects for maze simulation.
'''

# Import modules.
import numpy as np
import pygame

# Import classes, functions and values.
from objects import Ball, Wall, Maze
from settings import Position, Velocity

# Default ball settings.
DefaultBall = Ball(
    Position, # [mm]
    Velocity, # [mm/s]
)

# Default maze setting.
DefaultMaze = Maze(DefaultBall, [], [], [])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
