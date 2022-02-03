#!/usr/bin/env python3

# Import modules.
import pygame
import numpy as np

# Import classes, functions and values.
from functions import tilt_maze, generate_balls, generate_walls
from settings import FrameSize, PixelScale, White

# Initialise PyGame.
pygame.init()
# Initialise clocks.
Clock = pygame.time.Clock()
StepTimer = pygame.time.Clock()
# Initialise display.
Screen = pygame.display.set_mode([FrameSize[0] * PixelScale, FrameSize[1] * PixelScale])
pygame.display.set_caption('Maze Simulation')

# Create initial objects.
BallList = generate_balls()
WallList = generate_walls()

# Theta (radians) should be a size 2 vector of floats.
Theta = np.array([0.0, 0.0])

# Start simulation.
SimulationRunning = 1
while SimulationRunning == 1:

    # Check for events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            SimulationRunning = 0
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            # Manual maze tilt.
            Theta = tilt_maze(event, Theta)

    # Update ball.
    BallList.update(StepTimer.tick_busy_loop(), Theta, WallList) # Time step given in ms.

    # Update graphics
    Screen.fill(White)
    WallList.draw(Screen)
    BallList.draw(Screen)
    pygame.display.flip()

    Clock.tick()
    #Enable below to print T or fps.
    #print("{:.0f}ms".format(Clock.get_time()))
    #print("{:.0f}fps".format(1/Clock.get_time()*1000))

pygame.quit()