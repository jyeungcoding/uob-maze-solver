#!/usr/bin/env python3

# Import modules.
import pygame
import numpy as np

# Import classes, functions and values.
from objects import Ball, Wall
from settings import FrameSize, MazeSize, PixelScale, ThetaStep, BallStartingPosition, BallStartingVelocity, BallStartingAcceleration, BallRadius, BallMass, Drag

def generate_balls():
    # Generate initial balls.
    BallList = pygame.sprite.Group()
    ball = Ball(
        BallStartingPosition, # Standard units (see settings).
        BallStartingVelocity, # Standard units (see settings).
        BallStartingAcceleration, # Standard units (see settings).
        BallRadius, # Standard units (see settings).
        BallMass, # Standard units (see settings).
        Drag # Standard units (see settings).
    )
    BallList.add(ball)
    return BallList

def generate_walls():
    # Generate initial walls.
    WallList = pygame.sprite.Group()

    FrameHorizontal = (FrameSize[1] - MazeSize[1]) / 2 # Standard units (see settings).
    FrameVertical = (FrameSize[0] - MazeSize[0]) / 2

    Wall1 = Wall(
        np.array([0, 0]), # Standard units (see settings).
        np.array([FrameVertical, FrameSize[1]]) # Standard units (see settings).
    )
    Wall2 = Wall(
        np.array([FrameSize[0] - FrameVertical, 0]),
        np.array([FrameVertical, FrameSize[1]])
    )
    Wall3 = Wall(
        np.array([0, 0]),
        np.array([FrameSize[0], FrameHorizontal])
    )
    Wall4 = Wall(
        np.array([0, FrameSize[1] - FrameHorizontal]),
        np.array([FrameSize[0], FrameHorizontal])
    )
    WallList.add(Wall1, Wall2, Wall3, Wall4)
    return WallList

def tilt_maze(event, Theta):
    # Manual maze tilt using arrow keys.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            Theta[0] -= ThetaStep
        elif event.key == pygame.K_RIGHT:
            Theta[0] += ThetaStep
        elif event.key == pygame.K_UP:
            Theta[1] -= ThetaStep
        elif event.key == pygame.K_DOWN:
            Theta[1] += ThetaStep
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            Theta[0] += ThetaStep
        elif event.key == pygame.K_RIGHT:
            Theta[0] -= ThetaStep
        elif event.key == pygame.K_UP:
            Theta[1] += ThetaStep
        elif event.key == pygame.K_DOWN:
            Theta[1] -= ThetaStep
    return Theta

if __name__ == "__main__":
    import doctest
    doctest.testmod()