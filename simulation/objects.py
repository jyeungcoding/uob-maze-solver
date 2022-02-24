#!/usr/bin/env python3
'''
This file generates default objects for maze simulation and testing.
'''

# Import modules.
import numpy as np
from math import pi, sin, cos
import pygame

# Import classes, functions and values.
from objects import Ball, Wall, Hole, Checkpoint, Maze

# Sandbox Maze
SandboxBall = Ball(
    np.array([35.8, 40]), # [mm]
    np.array([0, 0]) # [mm/s]
)

SandboxWall = Wall(
    np.array([230, 80]),
    np.array([20, 20])
)

SandboxHole = Hole(np.array([80, 200]))

#SandboxCheckpoint = Checkpoint(np.array([166, 143]))
SandboxCheckpoint = Checkpoint(np.array([280, 240]))

SandboxMaze = Maze(SandboxBall, [SandboxWall], [SandboxHole], [SandboxCheckpoint])

# Circle Maze
CircleBall = Ball(
    np.array([50, 50]), # [mm]
    np.array([0, 0]) # [mm/s]
)

# Generate checkpoints in a circle
Circle = []
Theta = 0
while Theta < 2 * pi:
    Circle.append(Checkpoint(np.array([166 + 50 * sin(Theta), 143 + 50 * cos(Theta)])))
    Theta += pi / 8

CircleMaze = Maze(CircleBall, [], [], Circle)

# Simple Maze.
TestBall = Ball(
    np.array([50, 50]), # [mm]
    np.array([0, 0]) # [mm/s]
)

TestWalls = [
Wall(np.array([100, 28.25]), np.array([28.75, 170])),
Wall(np.array([200, 90]), np.array([28.75, 170]))
]

TestCheckpoints = [
Checkpoint(np.array([65, 50])),
Checkpoint(np.array([65, 220])),
Checkpoint(np.array([160, 220])),
Checkpoint(np.array([160, 50])),
Checkpoint(np.array([270, 50])),
Checkpoint(np.array([270, 220])),
]

SimpleMaze = Maze(TestBall, TestWalls, [], TestCheckpoints)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
