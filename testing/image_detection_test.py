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
from simulation.objects import SandboxMaze, SimpleMaze, CircleMaze
from image_detection.image_detection import Image_Detector
from control.timing_controller import TimingController
from graphics.graphics import initialise_background, initialise_checkpoints, initialise_ball, initialise_header, initialise_values, initialise_buttons
from settings import ControlPeriod, DisplayScale, White, Black

def image_detection_test():
    # Generate initial maze
    ActiveMaze = SandboxMaze

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
    Background = pygame.Surface((800 * DisplayScale, 480 * DisplayScale))
    Background.fill(White)
    BackgroundSprites = initialise_background(ActiveMaze.Holes, ActiveMaze.Walls)
    BackgroundSprites.draw(Background)
    Background.convert()

    # Generate checkpoints, outputs LayeredDirty group.
    ActiveSprites = initialise_checkpoints(ActiveMaze.Checkpoints)

    # Generate ball, add to ActiveSprites.
    SpriteBall_ = initialise_ball(ActiveMaze.Ball)
    ActiveSprites.add(SpriteBall_, layer = 1)

    # Initialise header, add to ActiveSprites.
    SpriteHeader = initialise_header()
    ActiveSprites.add(SpriteHeader, layer = 3)

    # Initialise output values, add to ActiveSprites.
    ActiveSprites.add(initialise_values(), layer = 2)

    # Initialise buttons, add to Buttons and ActiveSprites groups.
    Buttons = initialise_buttons()
    ActiveSprites.add(Buttons.sprites(), layer = 3)
    ''' PYGAME GRAPHICS END '''

    # Start main code.
    Running = 1
    # Start clock.
    StartTime = time.perf_counter() # Record start time.
    LastTime = StartTime # Temp.
    TimingController_ = TimingController(StartTime) # Start timing controller.

    ''' IMAGE DETECTION START '''
    # Initialise image detector.
    Cap = cv2.VideoCapture(0)
    #Cap.set(cv2.CAP_PROP_FPS, 10)
    ImageDetector = Image_Detector(StartTime)
    ''' IMAGE DETECTION END '''

    while Running == 1:

        ''' PYGAME EVENT HANDLER START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                X, Y = event.pos # Get position of click.
                for Button in Buttons:
                    if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                        # Check which button function to run.
                        if Button.CurrentState == "Quit": # Quit button quits the program.
                            Button.click(time.perf_counter()) # Animate button click.
                            Running = 0
        ''' PYGAME EVENT HANDLER END '''


        CurrentTime = time.perf_counter()
        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))
        #TimeStep = LastTime - CurrentTime
        #LastTime = CurrentTime

        ''' TIMING CONTROL START '''
        # Limit minimum time period between each control/graphics loop.
        ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(CurrentTime)
        ''' TIMING CONTROL END '''

        # Update ball position.
        ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, CurrentTime)

        # Generate strings for output values to be displayed.
        DisplayValues = {
        0 : "{0:.1f}".format(time.perf_counter() - StartTime), # Time elapsed.
        1 : "( {0:.1f} , {1:.1f} )".format(ActiveMaze.Ball.S[0], ActiveMaze.Ball.S[1]), # Ball position.
        }

        ''' PYGAME GRAPHICS START '''
        if GraphicsOn == True:
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

            # Update text sprites with new values.
            SpriteOutputValues = ActiveSprites.get_sprites_from_layer(2) # List of value text sprites.
            for Key in DisplayValues:
                SpriteOutputValues[Key].update(DisplayValues[Key])

            # Update button animations.
            Buttons.update(time.perf_counter())

        # Update changed areas.
        Rects = ActiveSprites.draw(Screen, Background)
        pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
        ''' PYGAME GRAPHICS END '''

    pygame.quit()

if __name__ == "__main__":
    image_detection_test()
