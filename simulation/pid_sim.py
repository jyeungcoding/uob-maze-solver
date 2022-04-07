#!/usr/bin/env python3
'''
This file contains PID_sim() which simulates PID control of the maze using the PID
controller in control/pid_controller.py.
'''

# Import modules.
import pygame
import numpy as np
import time
from math import degrees
from copy import deepcopy

# Import classes, functions and values.
from mazes import Maze1, Maze2, Maze3
from objects import Maze
from graphics.graphics import initialise_background, initialise_dirty_group, initialise_buttons, initialise_header, initialise_values, initialise_ball, change_maze
from control.pid_controller import PID_Controller
from control.calibrator import Calibrator
from control.timing_controller import TimingController
from control.performance_log import PerformanceLog
from motor_control.motor_control import motor_reset, motor_angle
from settings import MaxFrequency, DisplayScale, White, Black, Kp, Ki, Kd, Ks, Kst, BufferSize, SaturationLimit, MinTheta

def pid_sim():

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
            PID_Controller_ = PID_Controller(Kp, Ki, Kd, Ks, Kst, ActiveMaze.Checkpoints[0].S, BufferSize, SaturationLimit, MinTheta)
            ''' INITIALISE PID CONTROL '''

            ''' INITIALISE CALIBRATOR '''
            Calibrator_ = Calibrator() # Initialise SimulationTime
            ControlSignal = np.array([0, 0]) # Start at 0.
            ControlSignalCalibrated = np.array([0, 0]) # Record theta for 'true' level after calibration.
            ''' INITIALISE CALIBRATOR '''

            ''' INITIALISE MOTOR CONTROL '''
            #motor_reset()
            ''' INITIALISE MOTOR CONTROL '''

            # Starting values.
            ControlSignal = np.array([0.0, 0.0])
            Theta = np.array([0.0, 0.0]) # Theta (radians) should be a size 2 vector of floats.
            Saturation = np.array([False, False])
            PID_Output = [np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0])]

            # Start clock.
            TimeElapsed = 0
            StartTime = time.perf_counter() # Record start time.
            SimulationTime = StartTime # Initialise SimulationTime
            TimingController_ = TimingController(StartTime) # Start timing controller.
            PerformanceLog_ = PerformanceLog(StartTime) # Performance log. See control/performance_log.py for more information.
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

                ''' MAZE SIMULATION START '''
                # Calculate simulation loop time-step.
                LastSimulationTime = SimulationTime
                SimulationTime = time.perf_counter()
                TimeStep = SimulationTime - LastSimulationTime

                # Simulate next step of maze using theta and a given timestep.
                Output = ActiveMaze.next_step(TimeStep, Theta) # Time step given in s.

                if Output[0] == False:
                    BallLost = 1 # If ball is lost.
                ''' MAZE SIMULATION END '''

                ''' TIMING CONTROL START '''
                # Limit minimum time period between each control/graphics loop.
                ControlOn, ControlTimeStep, GraphicsOn = TimingController_.update(time.perf_counter())
                ''' TIMING CONTROL END '''

                if ControlOn == True:
                    ''' PID CONTROL START '''
                    if Output[0] == True: # Check active.
                        # Set ProcessVariable as the ball's position.
                        ProcessVariable = Output[1]

                        if CalibrationDone == 0:
                            ''' CALIBRATION START '''
                            # Calibrate to record level theta.
                            CalibrationDone, ControlSignalCalibrated = Calibrator_.update(ActiveMaze.Ball.S, ControlSignal, time.perf_counter())
                            if CalibrationDone == True:
                                PID_Controller_.calibrate(ControlSignalCalibrated) # Enter calibrated angle when done.
                            ''' CALIBRATION END '''
                        else:
                            # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
                            if ((ActiveMaze.Checkpoints[0].S[0] - ActiveMaze.Ball.S[0]) ** 2 + (ActiveMaze.Checkpoints[0].S[1] - ActiveMaze.Ball.S[1]) ** 2) ** 0.5 < 2:
                                if len(ActiveMaze.Checkpoints) > 1:
                                    ActiveMaze.Checkpoints.pop(0) # Delete current checkpoint.
                                    PID_Controller_.new_setpoint(ActiveMaze.Checkpoints[0].S) # Assign new set point.
                                elif len(ActiveMaze.Checkpoints) == 1:
                                    Completed = 1 # If the last checkpoint has been reached, the program has been completed.

                        # Calculate control signal using the PID controller.
                        PID_Output = PID_Controller_.update(ProcessVariable, ControlTimeStep)
                        Saturation = PID_Controller_.Saturation # For display.
                        ControlSignal = PID_Output[0]

                        # Convert control signal into actual Theta (based on measurements).
                        Theta = ControlSignal * np.array([3 / 20, 0.1])
                    ''' PID CONTROL END'''

                    ''' MOTOR CONTROL START'''
                    # Change the servo motors' angles.
                    #motor_angle(ControlSignal)
                    ''' MOTOR CONTROL END '''

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

                LogEntry = PerformanceLog_.update(ControlOn, GraphicsOn, time.perf_counter())
                # Enable below to print the timestep of a full loop. Note that this is very CPU intensive!
                #print(LogEntry)

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
                                        SystemRunning, Paused, Completed, CalibrationDone = 0, 0, 0, 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ProgramOn, SystemRunning, Paused = 0, 0, 0
                    ''' PYGAME EVENT HANDLER END '''

                    ''' MAZE SIMULATION START '''
                    # Calculate simulation loop time-step.
                    LastSimulationTime = SimulationTime
                    SimulationTime = time.perf_counter()
                    TimeStep = SimulationTime - LastSimulationTime

                    # Simulate next step of maze using theta and a given timestep.
                    Output = ActiveMaze.next_step(TimeStep, Theta) # Time step given in s.
                    ''' MAZE SIMULATION END '''

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
                    SpriteHeader.update("Ball Lost / Not Found")
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
                                        SystemRunning, BallLost, Completed, CalibrationDone = 0, 0, 0, 0
                                    elif Button.CurrentState == "Quit": # Quit button quits the program.
                                        Button.click(time.perf_counter()) # Animate button click.
                                        ProgramOn, SystemRunning, BallLost = 0, 0, 0
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

    PerformanceLog_.export("log.txt") # Export performance log.

if __name__ == "__main__":
    pid_sim()
