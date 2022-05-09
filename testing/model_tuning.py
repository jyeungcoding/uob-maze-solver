#!/usr/bin/env python3
'''
This file contains the function that simulates manual tilting of the maze
in the x direction for a specified time. Use to tune maze simulation physics.
'''

# Import modules.
import pygame
import numpy as np
import time
from math import degrees, pi

# Import classes, functions and values.
from objects import Maze
from graphics.graphics import initialise_background, initialise_dirty_group, initialise_buttons, initialise_header, initialise_values, initialise_ball, change_maze
from simulation.tilt_maze import tilt_maze
from simulation.objects import SandboxMaze
from settings import DisplayScale, White, Black

def model_tuning():

    # Generate starting maze.
    ActiveMaze = SandboxMaze

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("MazeModel should be of class Maze. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise clock for limiting framerate during the menu screens.
    Clock = pygame.time.Clock()
    # Initialise display surface.
    Screen = pygame.display.set_mode((800 * DisplayScale, 480 * DisplayScale))
    #Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Fullscreen mode: only use on pi touchscreen.
    pygame.display.set_caption("PID Simulation")

    # Generate background.
    Background = initialise_background((800 * DisplayScale, 480 * DisplayScale))

    # Create Dirty Sprite Group with holes, walls, checkpoints and keys.
    ActiveSprites = initialise_dirty_group(ActiveMaze)

    # Generate buttons, add to Buttons and ActiveSprites groups.
    Buttons = initialise_buttons()
    ActiveSprites.add(Buttons.sprites(), layer = 5)

    # Generate header, add to ActiveSprites.
    SpriteHeader = initialise_header()
    ActiveSprites.add(SpriteHeader, layer = 6)

    # Generate output values, add to ActiveSprites.
    ActiveSprites.add(initialise_values(), layer = 4)

    # Generate ball, add to ActiveSprites.
    SpriteBall_ = initialise_ball(ActiveMaze.Ball)
    ActiveSprites.add(SpriteBall_, layer = 7)
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
        ''' PYGAME GRAPHICS START '''
        # Update header.
        SpriteHeader.update("Running")
        ''' PYGAME GRAPHICS END '''

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

        ''' PYGAME EVENT HANDLER START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0
        ''' PYGAME EVENT HANDLER END '''

        # Generate strings for output values to be displayed.
        DisplayValues = {
        0 : "{0:.1f}".format(time.perf_counter() - StartTime), # Time elapsed.
        1 : "( {0:.1f} , {1:.1f} )".format(ActiveMaze.Ball.S[0], ActiveMaze.Ball.S[1]), # Ball position.
        7 : "( {0:.1f} , {1:.1f} )".format(degrees(Theta[0]), degrees(Theta[1])) # Theta.
        }

        ''' PYGAME GRAPHICS START '''
        # Update Sprite Ball position.
        if ActiveMaze.Ball.Active == True:
            SpriteBall_.update(ActiveMaze.Ball.S)
        else:
            SpriteBall_.kill()

        # Check/update SpriteSetPoint.
        while len(ActiveMaze.Checkpoints) < len(ActiveSprites.get_sprites_from_layer(2)):
            if len(ActiveSprites.get_sprites_from_layer(2)) != 1:
                ActiveSprites.get_sprites_from_layer(2)[1].update("SetPoint") # Change next checkpoint to set point.
            ActiveSprites.get_sprites_from_layer(2)[0].kill() # Remove previous set point.

        # Update text sprites with new values.
        SpriteOutputValues = ActiveSprites.get_sprites_from_layer(4) # List of value text sprites.
        CheckKey = len(SpriteOutputValues)
        for Key in DisplayValues:
            if Key < CheckKey: # Check if index exists.
                SpriteOutputValues[Key].update(DisplayValues[Key])

        # Update button animations.
        Buttons.update(time.perf_counter())

        # Update changed areas.
        Rects = ActiveSprites.draw(Screen, Background)
        pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
        ''' PYGAME GRAPHICS END '''

        # Calculate time elapsed in simulation loop.
        LastTime = CurrentTime
        CurrentTime = time.perf_counter()
        TimeStep = CurrentTime - LastTime
        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))

    pygame.quit()
