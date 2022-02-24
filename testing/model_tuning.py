#!/usr/bin/env python3
'''
This file contains the function that simulates manual tilting of the maze
with the arrow keys to ThetaStep in each direction. Utilises pyagme to
display graphics.
'''

# Import modules.
import pygame
import numpy as np
import time
from math import pi

# Import classes, functions and values.
from objects import Maze
from graphics.objects import SpriteBall, SpriteSetPoint
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from simulation.tilt_maze import tilt_maze
from simulation.objects import SandboxMaze
from settings import PixelScale, White, Black

def model_tuning():

    # Generate starting maze.
    ActiveMaze = SandboxMaze

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("MazeModel should be of class Maze. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise display surface.
    Screen = pygame.display.set_mode((ActiveMaze.Size[0] * PixelScale, (ActiveMaze.Size[1] + 33) * PixelScale))
    pygame.display.set_caption("Maze Simulation")

    # Initialise text module.
    pygame.font.init()
    # Create fonts.
    Font1 = pygame.font.SysFont("Times New Roman", 7 * PixelScale)

    # Generate graphic objects.
    # Generate ball.
    BallList = pygame.sprite.Group()
    SpriteBall1 = SpriteBall(
        ActiveMaze.Ball.S, # [mm], numpy vector, size 2.
        ActiveMaze.Ball.R, # [mm], numpy vector, size 2.
    )
    BallList.add(SpriteBall1)
    # Generate walls.
    WallList = initialise_walls(ActiveMaze.Walls)
    # Generate holes.
    HoleList = initialise_holes(ActiveMaze.Holes)
    # Generate checkpoints.
    CheckpointList = initialise_checkpoints(ActiveMaze.Checkpoints)

    # Set the first SpriteCheckpoint as the SpriteSetPoint and remove it from CheckpointList so it isn't drawn twice.
    CheckpointIter1 = iter(CheckpointList) # Sprite groups aren't indexed, so it is necessary to create an iterable.
    CheckpointIter2 = iter(CheckpointList)
    SpriteSetPoint1 = SpriteSetPoint(next(CheckpointIter1).S) # Set point is drawn red instead of blue.
    next(CheckpointIter2).kill()
    ''' PYGAME GRAPHICS END '''

    # Theta (radians) should be a size 2 vector of floats.
    Theta = np.array([0.0, 0.0])

    SetPoint = ActiveMaze.Checkpoints[0].S # Set set point as first checkpoint.

    # Start simulation loop.
    Running = 1
    # Start clock for time-steps.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.
    StartTime = CurrentTime # Record start time
    TimeStep = 0
    while Running == 1:

        Clock = CurrentTime - StartTime
        if Clock < 1:
            Theta = np.array([0.0, 0.0])
        elif Clock < 1.5:
            Theta = np.array([0.0111 * pi, 0.0])
        else:
            Theta = np.array([0.0, 0.0])

        # Simulate next step of maze using theta and a given timestep.
        Output = ActiveMaze.next_step(TimeStep, Theta) # Time step given in s.

        # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
        if ((SetPoint[0] - ActiveMaze.Ball.S[0]) ** 2 + (SetPoint[1] - ActiveMaze.Ball.S[1]) ** 2) ** 0.5 < 2 and len(ActiveMaze.Checkpoints) > 1:
            ActiveMaze.Checkpoints.pop(0)
            SetPoint = ActiveMaze.Checkpoints[0].S

        ''' PYGAME GRAPHICS START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0

        # Update Sprite Ball position.
        if ActiveMaze.Ball.Active == True:
            SpriteBall1.rect.centerx = ActiveMaze.Ball.S[0] * PixelScale # Ball position in pixels based on center of ball.
            SpriteBall1.rect.centery = ActiveMaze.Ball.S[1] * PixelScale # Ball position in pixels based on center of ball.
        else:
            SpriteBall1.kill()

        # Check/update SpriteSetPoint, remove last SpriteCheckpoint if necessary.
        while (len(ActiveMaze.Checkpoints) < len(CheckpointList) + 1) and len(ActiveMaze.Checkpoints) > 0:
            SpriteSetPoint1 = SpriteSetPoint(next(CheckpointIter1).S)
            next(CheckpointIter2).kill()

        # Create surface with text describing the ball's position.
        BallPositionTxt = Font1.render(str(ActiveMaze.Ball), False, Black)
        # Create surface with text displaying theta in degrees.
        ThetaTxt = Font1.render("Theta: %s" % (np.round(Theta * 360 / (2 * pi), 1)), False, Black)

        # Update graphics. Could optimise.
        Screen.fill(White)
        WallList.draw(Screen) # Draw walls.
        HoleList.draw(Screen) # Draw holes.
        CheckpointList.draw(Screen) # Draw checkpoints.
        Screen.blit(SpriteSetPoint1.image, SpriteSetPoint1.rect) # Draw set point.
        BallList.draw(Screen) # Draw ball.
        # Blit text to screen.
        Screen.blit(BallPositionTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 6) * PixelScale))
        Screen.blit(ThetaTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 17) * PixelScale))
        pygame.display.flip() # Update display.
        ''' PYGAME GRAPHICS END '''

        # Calculate time elapsed in simulation loop.
        LastTime = CurrentTime
        CurrentTime = time.perf_counter()
        TimeStep = CurrentTime - LastTime
        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))

    pygame.quit()
