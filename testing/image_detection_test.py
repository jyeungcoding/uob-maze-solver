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
from copy import deepcopy

# Import classes, functions and values.
from mazes import Maze1, Maze2, Maze3
from objects import Maze
from graphics.graphics import initialise_background, initialise_dirty_group, initialise_buttons, initialise_header, initialise_values, initialise_ball, change_maze
from image_detection.image_detection import Image_Detector
from control.timing_controller import TimingController
from control.timer import PerformanceTimer
from graphics.graphics import initialise_background, initialise_checkpoints, initialise_ball, initialise_header, initialise_values, initialise_buttons
from settings import DisplayScale, White

def image_detection_test():

    ''' ------ MENU SCREEN START ------ '''
    # Set starting maze.
    CurrentMaze = Maze1

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
    ActiveSprites = initialise_dirty_group(CurrentMaze)

    # Generate buttons, add to Buttons and ActiveSprites groups.
    Buttons = initialise_buttons()
    ActiveSprites.add(Buttons.sprites(), layer = 5)

    # Generate header, add to ActiveSprites.
    SpriteHeader = initialise_header()
    ActiveSprites.add(SpriteHeader, layer = 6)
    ''' PYGAME GRAPHICS END '''

    # Start program.
    ProgramOn = 1 # 1 while main program is running.
    SystemRunning = 0 # 1 while control system is running.
    CalibrationDone = 0 # 1 when calibration is done.
    Paused = 0 # 1 when paused.
    BallLost = 0 # 1 when ball is lost.
    Completed = 0 # 1 when maze is completed.
    while ProgramOn == 1:

        ''' PYGAME GRAPHICS START '''
        # Update header to ready.
        SpriteHeader.update("Ready")
        ''' PYGAME GRAPHICS END '''

        ''' PYGAME EVENT HANDLER START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ProgramOn = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                X, Y = event.pos # Get position of click.
                for Button in Buttons:
                    if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                        # Check which button function to run.
                        if Button.CurrentState == "Start":
                            Button.click(time.perf_counter()) # Animate button click.
                            SystemRunning = 1
                        elif Button.CurrentState == "Maze 1" or Button.CurrentState == "Maze 2" or Button.CurrentState == "Maze 3":
                            if Button.CurrentState == "Maze 1":
                                CurrentMaze = Maze2
                            elif Button.CurrentState == "Maze 2":
                                CurrentMaze = Maze3
                            elif Button.CurrentState == "Maze 3":
                                CurrentMaze = Maze1
                            Button.click(time.perf_counter()) # Animate button click.
                            change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                        elif Button.CurrentState == "Quit": # Quit button quits the program.
                            Button.click(time.perf_counter()) # Animate button click.
                            ProgramOn = 0
        ''' PYGAME EVENT HANDLER END '''

        ''' PYGAME GRAPHICS START '''
        # Update button animations.
        Buttons.update(time.perf_counter())
        # Update changed areas.
        Rects = ActiveSprites.draw(Screen, Background)
        pygame.display.update(Rects)
        Clock.tick(10) # Limit to 10fps to conserve processing power.
        ''' PYGAME GRAPHICS END '''

        ''' ------ MENU SCREEN END ------ '''


        ''' ------ RUNNING SCREEN START ------ '''

        # Run system if SystemRunning == 1.
        if SystemRunning == 1:

            # Set ActiveMaze as a copy of CurrentMaze.
            ActiveMaze = deepcopy(CurrentMaze)

            # Check ActiveMaze is correct type.
            if type(ActiveMaze) != Maze:
                raise TypeError("ActiveMaze should be of class Maze. See 'objects.py'.")
            if len(ActiveMaze.Checkpoints) == 0:
                raise ValueError("No checkpoints found.")

            ''' PYGAME GRAPHICS START '''
            # Generate output values, add to ActiveSprites.
            ActiveSprites.add(initialise_values(), layer = 4)
            # Generate ball, add to ActiveSprites.
            SpriteBall_ = initialise_ball(ActiveMaze.Ball)
            ActiveSprites.add(SpriteBall_, layer = 7)
            ''' PYGAME GRAPHICS END '''

            # Start clock.
            StartTime = time.perf_counter() # Record start time.
            TimingController_ = TimingController(StartTime) # Start timing controller.
            PerformanceTimer_ = PerformanceTimer(StartTime) # Performance timer for measuring time period of each loop.

            ''' IMAGE DETECTION START '''
            # Initialise image detector.
            Cap = cv2.VideoCapture(0)
            #Cap.set(cv2.CAP_PROP_FPS, 10)
            ImageDetector = Image_Detector(StartTime)
            ''' IMAGE DETECTION END '''

            while SystemRunning == 1:

                ''' PYGAME GRAPHICS START '''
                # Update header.
                SpriteHeader.update("Running")
                ''' PYGAME GRAPHICS END '''

                ''' PYGAME EVENT HANDLER START '''
                # Check for events.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ProgramOn = 0
                        SystemRunning = 0
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        X, Y = event.pos # Get position of click.
                        for Button in Buttons:
                            if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                                # Check which button function to run.
                                if Button.CurrentState == "Stop":
                                    Button.click(time.perf_counter()) # Animate button click.
                                    Paused = 1
                                elif Button.CurrentState == "Reset":
                                    Button.click(time.perf_counter()) # Animate button click.
                                    Buttons.get_sprite(0).click(time.perf_counter()) # Change stop button to start.
                                    ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                    ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                    SpriteBall_.kill() # Erase ball.
                                    SystemRunning = 0
                                elif Button.CurrentState == "Quit": # Quit button quits the program.
                                    Button.click(time.perf_counter()) # Animate button click.
                                    ProgramOn = 0
                                    SystemRunning = 0
                ''' PYGAME EVENT HANDLER END '''

                ''' IMAGE DETECTION START '''
                # Update ball position.
                ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, time.perf_counter())
                if ActiveMaze.Ball.Active == False:
                    BallLost = 1 # If ball is lost.
                ''' IMAGE DETECTION END '''

                ''' TIMING CONTROL START '''
                # Limit minimum time period between each control/graphics loop.
                ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(time.perf_counter())
                ''' TIMING CONTROL END '''

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

                # Enable below to print the timestep of a full loop.
                #print("{:.0f}ms".format(PerformanceTimer_.update(time.perf_counter()) * 1000))

                ''' ------ RUNNING SCREEN END ------ '''


                ''' ------ PAUSED SCREEN START ------ '''

                while Paused == 1:

                    ''' PYGAME GRAPHICS START '''
                    # Update header.
                    SpriteHeader.update("Paused")
                    ''' PYGAME GRAPHICS END '''

                    ''' PYGAME EVENT HANDLER START '''
                    # Check for events.
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            ProgramOn = 0
                            SystemRunning = 0
                            Paused = 0
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            X, Y = event.pos # Get position of click.
                            for Button in Buttons:
                                if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                                    # Check which button function to run.
                                    if Button.CurrentState == "Start":
                                        Button.click(time.perf_counter()) # Animate button click.
                                        Paused = 0
                                    elif Button.CurrentState == "Reset":
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                        ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                        SpriteBall_.kill() # Erase ball.
                                        SystemRunning = 0
                                        Paused = 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ProgramOn = 0
                                        SystemRunning = 0
                                        Paused = 0
                    ''' PYGAME EVENT HANDLER END '''

                    ''' IMAGE DETECTION START '''
                    # Update ball position.
                    ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, time.perf_counter())
                    if ActiveMaze.Ball.Active == False:
                        BallLost = 1 # If ball is lost.
                    ''' IMAGE DETECTION END '''

                    ''' TIMING CONTROL START '''
                    # Limit minimum time period between each control/graphics loop.
                    ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(time.perf_counter())
                    ''' TIMING CONTROL END '''

                    ''' PYGAME GRAPHICS START '''
                    if GraphicsOn == True:
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

                    # Update button animations.
                    Buttons.update(time.perf_counter())

                    # Update changed areas.
                    Rects = ActiveSprites.draw(Screen, Background)
                    pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
                    ''' PYGAME GRAPHICS END '''

                ''' ------ PAUSED SCREEN END ------ '''


                ''' ------ BALL LOST SCREEN START ------ '''

                while BallLost == 1:

                    ''' PYGAME GRAPHICS START '''
                    # Update header.
                    SpriteHeader.update("Ball Lost")
                    ''' PYGAME GRAPHICS END '''

                    ''' PYGAME EVENT HANDLER START '''
                    # Check for events.
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            ProgramOn = 0
                            SystemRunning = 0
                            BallLost = 0
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            X, Y = event.pos # Get position of click.
                            for Button in Buttons:
                                if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                                    # Check which button function to run.
                                    if Button.CurrentState == "Reset":
                                        Button.click(time.perf_counter()) # Animate button click.
                                        Buttons.get_sprite(0).click(time.perf_counter()) # Change stop button to start.
                                        ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                        ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                        SpriteBall_.kill() # Erase ball.
                                        SystemRunning = 0
                                        BallLost = 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ProgramOn = 0
                                        SystemRunning = 0
                                        BallLost = 0
                    ''' PYGAME EVENT HANDLER END '''

                    ''' PYGAME GRAPHICS START '''
                    # Update button animations.
                    Buttons.update(time.perf_counter())

                    # Update changed areas.
                    Rects = ActiveSprites.draw(Screen, Background)
                    pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
                    Clock.tick(10) # Limit to 10fps to conserve processing power.
                    ''' PYGAME GRAPHICS END '''

                ''' ------ BALL LOST SCREEN END ------ '''

    pygame.quit()

if __name__ == "__main__":
    image_detection_test()
