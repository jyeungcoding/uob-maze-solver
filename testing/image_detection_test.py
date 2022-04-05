#!/usr/bin/env python3
'''
This file contains a function that captures the state of the physical maze with the
image detection functions in image_detection/image_detection.py and displays it on
screen using the pygame module.
'''

# Import modules.
from picamera.array import PiRGBArray # Allows conversion of frames to cv2 array format.
from picamera import PiCamera
import cv2
import pygame
import numpy as np
from time import sleep, perf_counter
from copy import deepcopy

# Import classes, functions and values.
from mazes import Maze1, Maze2, Maze3
from objects import Maze, Ball
from graphics.graphics import initialise_background, initialise_dirty_group, initialise_buttons, initialise_header, initialise_values, initialise_ball, change_maze
from control.timing_controller import TimingController
from image_detection.image_detection import ImageProcessor
from control.timer import PerformanceTimer
from graphics.graphics import initialise_background, initialise_checkpoints, initialise_ball, initialise_header, initialise_values, initialise_buttons
from settings import MaxFrequency, DisplayScale, White, MazeSize, HSVLimitsBlue, HSVLimitsGreen

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
                            Button.click(perf_counter()) # Animate button click.
                            SystemRunning = 1
                        elif Button.CurrentState == "Maze 1" or Button.CurrentState == "Maze 2" or Button.CurrentState == "Maze 3":
                            if Button.CurrentState == "Maze 1":
                                CurrentMaze = Maze2
                            elif Button.CurrentState == "Maze 2":
                                CurrentMaze = Maze3
                            elif Button.CurrentState == "Maze 3":
                                CurrentMaze = Maze1
                            Button.click(perf_counter()) # Animate button click.
                            change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                        elif Button.CurrentState == "Quit": # Quit button quits the program.
                            Button.click(perf_counter()) # Animate button click.
                            ProgramOn = 0
        ''' PYGAME EVENT HANDLER END '''

        ''' PYGAME GRAPHICS START '''
        # Update button animations.
        Buttons.update(perf_counter())
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
            SpriteBall_ = initialise_ball(Ball(np.array([-20, -20])))
            ActiveSprites.add(SpriteBall_, layer = 7)
            ''' PYGAME GRAPHICS END '''

            """ PICAMERA INITIALISATION START """
            # Initialise the camera.
            # Set sensor mode to 4. Refer to Raspicam documentation. Size: 1640x1232, framerate: 40fps.
            Camera = PiCamera(sensor_mode = 4) # See if fixing the camera settings improves performance.
            # Camera.framerate = 20 # Can set the camera's framerate.
            # Create an object containing an array in the correct openCV format to store each frame. The camera arg just saves a reference to the camera.
            Capture = PiRGBArray(Camera, size = (640, 480)) # Size should be the same as the size of the input frames.
            sleep(0.2) # Wait for the camera to warm up.
            # Outputs an infinite iterable that inserts the next frame into Capture as the output every time you call it.
            # Change frame format to BGR (for openCV) and resize it to (640, 480) for faster processing. Use video port for faster frame capture.
            Frames = Camera.capture_continuous(Capture, format = "bgr", resize = (640, 480), use_video_port = True)
            """ PICAMERA INITIALISATION END """

            # Start clock.
            StartTime = perf_counter() # Record start time.
            TimingController_ = TimingController(StartTime) # Start timing controller.
            PerformanceTimer_ = PerformanceTimer(StartTime) # Performance timer for measuring time period of each loop.

            """ IMAGE PROCESSOR INITIALISATION START """
            ImageProcessor_ = ImageProcessor(perf_counter(), MazeSize, HSVLimitsBlue, HSVLimitsGreen)
            """ IMAGE PROCESSOR INITIALISATION END """

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
                                    Button.click(perf_counter()) # Animate button click.
                                    Paused = 1
                                elif Button.CurrentState == "Reset":
                                    Button.click(perf_counter()) # Animate button click.
                                    Buttons.get_sprite(0).click(perf_counter()) # Change stop button to start.
                                    ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                    change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                                    ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                    SpriteBall_.kill() # Erase ball.
                                    SystemRunning = 0
                                elif Button.CurrentState == "Quit": # Quit button quits the program.
                                    Button.click(perf_counter()) # Animate button click.
                                    ProgramOn = 0
                                    SystemRunning = 0
                ''' PYGAME EVENT HANDLER END '''

                ''' TIMING CONTROL START '''
                # Limit minimum time period between each control/graphics loop.
                ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(perf_counter())
                ''' TIMING CONTROL END '''

                if ControlOn == True:
                    """ IMAGE CAPTURE START """
                    Capture.truncate(0) # Clear Capture so the next frame can be inserted.
                    Frame = next(Frames) # If there is a new frame, grab it.
                    Image = Frame.array # Store the array from the frame object.
                    """ IMAGE CAPTURE END """

                    ''' IMAGE DETECTION START '''
                    ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageProcessor_.update(perf_counter(), Image) # Find ball position.
                    if ActiveMaze.Ball.Active == False:
                        BallLost = 1 # If ball is lost.
                    ''' IMAGE DETECTION END '''

                # Generate strings for output values to be displayed.
                DisplayValues = {
                0 : "{0:.1f}".format(perf_counter() - StartTime), # Time elapsed.
                1 : "( {0:.1f} , {1:.1f} )".format(ActiveMaze.Ball.S[0], ActiveMaze.Ball.S[1]), # Ball position.
                }

                ''' PYGAME GRAPHICS START '''
                if GraphicsOn == True:
                    # Update Sprite Ball position.
                    if ActiveMaze.Ball.Active == True:
                        SpriteBall_.update(ActiveMaze.Ball.S)

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
                    Buttons.update(perf_counter())

                if ActiveMaze.Ball.Active == False:
                    SpriteBall_.kill()

                # Update changed areas.
                Rects = ActiveSprites.draw(Screen, Background)
                pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
                Clock.tick(MaxFrequency) # Limit to MaxFrequency to conserve processing power.
                ''' PYGAME GRAPHICS END '''

                # Enable below to print the timestep of a full loop.
                #print("{:.0f}ms".format(PerformanceTimer_.update(perf_counter()) * 1000))

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
                                        Button.click(perf_counter()) # Animate button click.
                                        Paused = 0
                                    elif Button.CurrentState == "Reset":
                                        Button.click(perf_counter()) # Animate button click.
                                        ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                        change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                                        ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                        SpriteBall_.kill() # Erase ball.
                                        SystemRunning = 0
                                        Paused = 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(perf_counter()) # Animate button click.
                                        ProgramOn = 0
                                        SystemRunning = 0
                                        Paused = 0
                    ''' PYGAME EVENT HANDLER END '''

                    ''' TIMING CONTROL START '''
                    # Limit minimum time period between each control/graphics loop.
                    ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(perf_counter())
                    ''' TIMING CONTROL END '''

                    if ControlOn == True:
                        """ IMAGE CAPTURE START """
                        Capture.truncate(0) # Clear Capture so the next frame can be inserted.
                        Frame = next(Frames) # If there is a new frame, grab it.
                        Image = Frame.array # Store the array from the frame object.
                        """ IMAGE CAPTURE END """

                        ''' IMAGE DETECTION START '''
                        ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageProcessor_.update(perf_counter(), Image) # Find ball position.
                        if ActiveMaze.Ball.Active == False:
                            BallLost = 1 # If ball is lost.
                            Paused = 0
                        ''' IMAGE DETECTION END '''

                    DisplayValues = {
                    0 : "{0:.1f}".format(perf_counter() - StartTime), # Time elapsed.
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
                    Buttons.update(perf_counter())

                    # Update changed areas.
                    Rects = ActiveSprites.draw(Screen, Background)
                    pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
                    Clock.tick(MaxFrequency) # Limit to MaxFrequency to conserve processing power.
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
                                        Button.click(perf_counter()) # Animate button click.
                                        Buttons.get_sprite(0).click(perf_counter()) # Change stop button to start.
                                        ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                        change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                                        ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                        SpriteBall_.kill() # Erase ball.
                                        SystemRunning = 0
                                        BallLost = 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(perf_counter()) # Animate button click.
                                        ProgramOn = 0
                                        SystemRunning = 0
                                        BallLost = 0
                    ''' PYGAME EVENT HANDLER END '''

                    ''' PYGAME GRAPHICS START '''
                    # Update button animations.
                    Buttons.update(perf_counter())

                    # Update changed areas.
                    Rects = ActiveSprites.draw(Screen, Background)
                    pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
                    Clock.tick(10) # Limit to 10fps to conserve processing power.
                    ''' PYGAME GRAPHICS END '''

                ''' ------ BALL LOST SCREEN END ------ '''

    pygame.quit()

if __name__ == "__main__":
    image_detection_test()
