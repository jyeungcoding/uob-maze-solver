#!/usr/bin/env python3
'''
This file contains our fully integrated system. Image detection, feedback control,
motor control, and the graphics are all implemented from modular functions.
'''

# Import modules.
from picamera.array import PiRGBArray # Allows conversion of frames to cv2 array format.
from picamera import PiCamera
import cv2
import pygame
import numpy as np
import time
from math import degrees
from copy import deepcopy

# Import classes, functions and values.
from mazes import Maze1, Maze2, Maze3
from objects import Maze
from graphics.graphics import initialise_background, initialise_dirty_group, initialise_buttons, initialise_header, initialise_values, initialise_ball, change_maze
from image_detection.image_detection import ImageProcessor
from control.pid_controller import PID_Controller
from control.calibrator import Calibrator
from control.timing_controller import TimingController
from control.timer import PerformanceTimer
from motor_control.motor_control import motor_reset, motor_angle
from settings import MaxFrequency, DisplayScale, White, Kp, Ki, Kd, BufferSize, SaturationLimit, MinSignal, MazeSize, HSVLimitsBlue, HSVLimitsGreen

def full_system():

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
    ProgramOn, SystemRunning, CalibrationDone, Paused, BallLost, Completed = 1, 0, 0, 0, 0, 0
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

            ''' INITIALISE PID CONTROL '''
            # Initialise PID controller object, see control/pid_controller.py for more information.
            PID_Controller_ = PID_Controller(Kp, Ki, Kd, ActiveMaze.Checkpoints[0].S, BufferSize, SaturationLimit, MinSignal)
            ''' INITIALISE PID CONTROL '''

            ''' INITIALISE CALIBRATOR '''
            Calibrator_ = Calibrator() # Initialise SimulationTime
            ControlSignal = np.array([0, 0]) # Start at 0.
            ControlSignalCalibrated = np.array([0, 0]) # Record control signal angle for 'true' level after calibration.
            ''' INITIALISE CALIBRATOR '''

            ''' INITIALISE MOTOR CONTROL '''
            motor_reset()
            ''' INITIALISE MOTOR CONTROL '''

            """ PICAMERA INITIALISATION START """
            # Initialise the camera.
            # Set sensor mode to 4. Refer to Raspicam documentation. Size: 1640x1232, framerate: 40fps.
            Camera = PiCamera(sensor_mode = 4) # See if fixing the camera settings improves performance.
            # Camera.framerate = 20 # Can set the camera's framerate.
            # Create an object containing an array in the correct openCV format to store each frame. The camera arg just saves a reference to the camera.
            Capture = PiRGBArray(Camera, size = (640, 480)) # Size should be the same as the size of the input frames.
            time.sleep(0.2) # Wait for the camera to warm up.
            # Outputs an infinite iterable that inserts the next frame into Capture as the output every time you call it.
            # Change frame format to BGR (for openCV) and resize it to (640, 480) for faster processing. Use video port for faster frame capture.
            Frames = Camera.capture_continuous(Capture, format = "bgr", resize = (640, 480), use_video_port = True)
            """ PICAMERA INITIALISATION END """

            # Start clock.
            TimeElapsed = 0
            StartTime = time.perf_counter() # Record start time.
            TimingController_ = TimingController(StartTime) # Start timing controller.
            PerformanceTimer_ = PerformanceTimer(StartTime) # Performance timer for measuring time period of each loop.

            """ IMAGE PROCESSOR INITIALISATION START """
            ImageProcessor_ = ImageProcessor(perf_counter(), MazeSize, HSVLimitsBlue, HSVLimitsGreen)
            """ IMAGE PROCESSOR INITIALISATION END """

            while SystemRunning == 1:

                ''' PYGAME GRAPHICS START '''
                # Update header.
                if CalibrationDone == 0:
                    SpriteHeader.update("Calibrating")
                else:
                    if Completed == 0:
                        SpriteHeader.update("Running")
                    else:
                        SpriteHeader.update("Completed")
                ''' PYGAME GRAPHICS END '''

                ''' PYGAME EVENT HANDLER START '''
                # Check for events.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        ProgramOn, SystemRunning = 0, 0
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
                                    change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                                    ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                    SpriteBall_.kill() # Erase ball.
                                    SystemRunning, Completed, CalibrationDone = 0, 0, 0
                                elif Button.CurrentState == "Quit": # Quit button quits the program.
                                    Button.click(time.perf_counter()) # Animate button click.
                                    ProgramOn, SystemRunning = 0, 0
                ''' PYGAME EVENT HANDLER END '''

                ''' TIMING CONTROL START '''
                # Limit minimum time period between each control/graphics loop.
                ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(time.perf_counter())
                ''' TIMING CONTROL END '''

                if ControlOn == True:
                    ''' IMAGE DETECTION START '''
                    ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageProcessor_.update(perf_counter(), Image) # Find ball position.
                    if ActiveMaze.Ball.Active == False:
                        BallLost = 1 # If ball is lost.
                    ''' IMAGE DETECTION END '''

                    ''' PID CONTROL START '''
                    if CalibrationDone == 0:
                        ''' CALIBRATION START '''
                        # Calibrate to record level theta.
                        CalibrationDone, ControlSignalCalibrated = Calibrator_.update(ActiveMaze.Ball.S, ControlSignal, time.perf_counter())
                        if CalibrationDone == True:
                            PID_Controller_.calibrate(ControlSignalCalibrated) # Enter calibrated angle when done.
                        ''' CALIBRATION START '''
                    else:
                        # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
                        if ((ActiveMaze.Checkpoints[0].S[0] - ActiveMaze.Ball.S[0]) ** 2 + (ActiveMaze.Checkpoints[0].S[1] - ActiveMaze.Ball.S[1]) ** 2) ** 0.5 < 2:
                            if len(ActiveMaze.Checkpoints) > 1:
                                ActiveMaze.Checkpoints.pop(0) # Delete current checkpoint.
                                PID_Controller_.new_setpoint(ActiveMaze.Checkpoints[0].S) # Assign new set point.
                            elif len(ActiveMaze.Checkpoints) == 1:
                                Completed = 1

                    # Calculate control signal using the PID controller.
                    PID_Output = PID_Controller_.update(ActiveMaze.Ball.S, ControlTimeStep)
                    Saturation = PID_Controller_.Saturation # For display.
                    ControlSignal = PID_Output[0]
                    ''' PID CONTROL END'''
                    # Make sure you deal with the cases where no control signal is generated when Active == False.
                    ''' MOTOR CONTROL START'''
                    # Change the servo motors' angles.
                    motor_angle(ControlSignal)
                    ''' MOTOR CONTROL END '''

                    # Convert control signal into actual Theta (based on measurements).
                    Theta = ControlSignal * np.array([3 / 20, 0.1]) # For display.

                if Completed == 0:
                    TimeElapsed = time.perf_counter() - StartTime

                # Generate strings for output values to be displayed.
                DisplayValues = {
                0 : "{0:.1f}".format(TimeElapsed), # Time elapsed.
                1 : "( {0:.1f} , {1:.1f} )".format(ActiveMaze.Ball.S[0], ActiveMaze.Ball.S[1]), # Ball position.
                2 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[1][0]), degrees(PID_Output[1][1])), # P.
                3 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[2][0]), degrees(PID_Output[2][1])), # I.
                4 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[3][0]), degrees(PID_Output[3][1])), # D.
                5 : "( {!s:^5} , {!s:^5} )".format(Saturation[0], Saturation[1]), # Saturation.
                6 : "( {0:.1f} , {1:.1f} )".format(degrees(ControlSignal[0]), degrees(ControlSignal[1])), # Control signal.
                7 : "( {0:.1f} , {1:.1f} )".format(degrees(Theta[0]), degrees(Theta[1])) # Theta.
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
                    Buttons.update(time.perf_counter())

                if ActiveMaze.Ball.Active == False:
                    SpriteBall_.kill()

                # Update changed areas.
                Rects = ActiveSprites.draw(Screen, Background)
                pygame.display.update(Rects) # Rects is empty if GraphicsOn == False.
                Clock.tick(MaxFrequency) # Limit to MaxFrequency to conserve processing power.
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
                            ProgramOn, SystemRunning, Paused = 0, 0, 0
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            X, Y = event.pos # Get position of click.
                            for Button in Buttons:
                                if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                                    # Check which button function to run.
                                    if Button.CurrentState == "Start":
                                        Button.click(time.perf_counter()) # Animate button click.
                                        PID_Controller_.reset() # Reset PID controller.
                                        Paused = 0
                                    elif Button.CurrentState == "Reset":
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                        change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                                        ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                        SpriteBall_.kill() # Erase ball.
                                        SystemRunning, Paused, Completed = 0, 0, 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ProgramOn, SystemRunning, Paused, CalibrationDone = 0, 0, 0, 0
                    ''' PYGAME EVENT HANDLER END '''

                    ''' IMAGE DETECTION START '''
                    # Capture and update position of ball.
                    ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, time.perf_counter())
                    if ActiveMaze.Ball.Active == False:
                        BallLost = 1 # If ball is lost.
                        Paused = 0
                    ''' IMAGE DETECTION END '''

                    ''' TIMING CONTROL START '''
                    # Limit minimum time period between each control/graphics loop.
                    ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(time.perf_counter())
                    ''' TIMING CONTROL END '''

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
                            ProgramOn, SystemRunning, BallLost = 0, 0, 0
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            X, Y = event.pos # Get position of click.
                            for Button in Buttons:
                                if Button.rect.collidepoint(X, Y): # Check for collision with buttons.
                                    # Check which button function to run.
                                    if Button.CurrentState == "Reset":
                                        Button.click(time.perf_counter()) # Animate button click.
                                        Buttons.get_sprite(0).click(time.perf_counter()) # Change stop button to start.
                                        ActiveMaze = deepcopy(CurrentMaze) # Reset maze.
                                        change_maze(ActiveSprites, CurrentMaze) # Reset certain Sprites.
                                        ActiveSprites.remove_sprites_of_layer(4) # Erase display values.
                                        SpriteBall_.kill() # Erase ball.
                                        SystemRunning, BallLost, Completed = 0, 0, 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ProgramOn, SystemRunning, BallLost, CalibrationDone = 0, 0, 0, 0
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
    full_system()
