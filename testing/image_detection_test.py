#!/usr/bin/env python3
'''
This file contains a function that captures the state of the physical maze with the
image detection functions in image_detection/image_detection.py and displays it on
screen using the pygame module.
'''

# Import modules.
import pygame
import time
import cv2

# Import classes, functions and values.
from objects import Maze, Ball
from image_detection.image_detection import Image_Detector
from graphics.graphics import initialise_background, initialise_checkpoints, initialise_ball, initialise_values
from settings import ControlPeriod, DisplayScale, White, Black

def image_detection_test():

    # Start clock for time-steps.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.
    StartTime = CurrentTime # Record start time. 

    # Initialise image detector.
    Cap = cv2.VideoCapture(0)
    #Cap.set(cv2.CAP_PROP_FPS, 10)
    ImageDetector = Image_Detector(CurrentTime)
    # Capture inital maze elements and ball position.
    ActiveMaze = ImageDetector.initialise_maze()

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("'initialise_maze' should return an object of Maze class. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise display surface.
    Screen = pygame.display.set_mode((800 * DisplayScale, 480 * DisplayScale))
    #Screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # Fullscreen mode: only use on pi touchscreen.
    pygame.display.set_caption("PID Simulation")

    # Generate background.
    Background = pygame.Surface((800 * DisplayScale, 480 * DisplayScale)).convert()
    Background.fill(White)
    BackgroundSprites = initialise_background(ActiveMaze.Holes, ActiveMaze.Walls)
    BackgroundSprites.draw(Background)

    # Generate checkpoints, outputs LayeredDirty group.
    ActiveSprites = initialise_checkpoints(ActiveMaze.Checkpoints)

    # Generate ball, add to ActiveSprites.
    SpriteBall_ = initialise_ball(ActiveMaze.Ball)
    ActiveSprites.add(SpriteBall_, layer = 1)

    # Initialise output values, add to ActiveSprites.
    ActiveSprites.add(initialise_values(), layer = 2)
    ''' PYGAME GRAPHICS END '''

    # Start main code.
    Running = 1
    while Running == 1:

        # Update clock, limit
        LastTime = CurrentTime
        CurrentTime = time.perf_counter()
        TimeStep = CurrentTime - LastTime # For measuring loop time.
        if CurrentTime - LastTime < ControlPeriod:
            time.sleep(ControlPeriod - CurrentTime + LastTime)
            CurrentTime = time.perf_counter()
            TimeStep = CurrentTime - LastTime # For measuring loop time.

        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))

        # Update ball position.
        ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, CurrentTime)

        ''' PYGAME EVENT HANDLER START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0
        ''' PYGAME EVENT HANDLER END '''

        ''' PYGAME GRAPHICS START '''
        # Update Sprite Ball position.
        if ActiveMaze.Ball.Active == True:
            SpriteBall_.update(ActiveMaze.Ball.S)
        else:
            SpriteBall_.kill()

        # Check/update SpriteSetPoint.
        while len(ActiveMaze.Checkpoints) < len(ActiveSprites.get_sprites_from_layer(0)):
            if len(ActiveSprites.get_sprites_from_layer(0)) != 1:
                ActiveSprites.get_sprites_from_layer(0)[1].update("SetPoint") # Change next checkpoint to set point.
            ActiveSprites.get_sprites_from_layer(0)[0].kill() # Remove previous set point.

        # Generate strings for output values to be displayed.
        OutputValues = {
        0 : "{0:.1f}".format(time.perf_counter() - StartTime), # Time elapsed.
        1 : "( {0:.1f} , {1:.1f} )".format(ActiveMaze.Ball.S[0], ActiveMaze.Ball.S[1]), # Ball position.
        }
        # Update text sprites with new values.
        Values = ActiveSprites.get_sprites_from_layer(2) # List of value text sprites.
        for Key in OutputValues:
            Values[Key].update(OutputValues[Key])

        # Update changed areas.
        Rects = ActiveSprites.draw(Screen, Background)
        pygame.display.update(Rects)
        ''' PYGAME GRAPHICS END '''

    pygame.quit()

if __name__ == "__main__":
    image_detection_test()
