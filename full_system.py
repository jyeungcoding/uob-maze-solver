#!/usr/bin/env python3
'''
This file contains our fully integrated system. Image detection, feedback control,
motor control, and the graphics are all implemented from modular functions.
'''

# Import modules.
import pygame
import cv2
import numpy as np
import time
from math import degrees

# Import classes, functions and values.
from objects import Maze
from graphics.graphics import initialise_background, initialise_checkpoints, initialise_ball, initialise_values
from image_detection.image_detection import Image_Detector
from control.pid_controller import PID_Controller
from motor_control.motor_control import motor_reset, motor_angle
from settings import ControlPeriod, GraphicsPeriod, DisplayScale, White, Black, Kp, Ki, Kd, BufferSize, SaturationLimit, MinSignal

def full_system():

    # Start clock.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.
    StartTime = CurrentTime # Record start time.
    LastTime = CurrentTime # For timing each full loop.
    LastFrameTime = CurrentTime # For timing each image frame loop.

    ''' IMAGE DETECTION START '''
    # Initialise image detector.
    Cap = cv2.VideoCapture(0)
    #Cap.set(cv2.CAP_PROP_FPS, 10)
    ImageDetector = Image_Detector(CurrentTime)
    # Capture inital maze elements and ball position.
    ActiveMaze = ImageDetector.initialise_maze()

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("ActiveMaze should be of class Maze. See 'objects.py'.")

    if len(ActiveMaze.Checkpoints) == 0:
        raise ValueError("No checkpoints detected.")
    ''' IMAGE DETECTION END '''

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

    ''' INITIALISE PID CONTROL '''
    # Initialise PID controller object, see control/pid_controller.py for more information.
    PID_Controller1 = PID_Controller(Kp, Ki, Kd, ActiveMaze.Checkpoints[0].S, BufferSize, SaturationLimit, MinSignal)
    ''' INITIALISE PID CONTROL '''

    ''' INITIALISE MOTOR CONTROL '''
    motor_reset()
    ''' INITIALISE MOTOR CONTROL '''

    # Start control program.
    Running = 1
    # Start clock for time-steps.
    ControlOn = True # Turns control on and off.
    LastControl = CurrentTime # Last time control signal was updated.
    GraphicsOn = True # Turns graphics on and off.
    LastGraphics = CurrentTime # Last time graphics were updated.
    while Running == 1:

        # Limit minimum time period between each control loop.
        CurrentTime = time.perf_counter()
        if CurrentTime - LastControl > ControlPeriod: # Time period in settings.
            ControlOn = True
            LastControl = CurrentTime
        else:
            ControlOn = False
        if CurrentTime - LastGraphics > GraphicsPeriod: # Time period in settings.
            GraphicsOn = True
            LastGraphics = CurrentTime
        else:
            GraphicsOn = False

        if ControlOn == True:
            ''' IMAGE DETECTION START '''
            # Capture and update position of ball.
            ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, CurrentTime)
            ''' IMAGE DETECTION END '''

            # Calculate time since last frame.
            CurrentTime = time.perf_counter()
            FrameTimeStep = CurrentTime - LastFrameTime
            LastFrameTime = CurrentTime

            ''' PID CONTROL START '''
            if ActiveMaze.Ball.Active == True:
                # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
                while ((ActiveMaze.Checkpoints[0].S[0] - ActiveMaze.Ball.S[0]) ** 2 + (ActiveMaze.Checkpoints[0].S[1] - ActiveMaze.Ball.S[1]) ** 2) ** 0.5 < 2 and len(ActiveMaze.Checkpoints) > 1:
                    ActiveMaze.Checkpoints.pop(0)
                    PID_Controller1.new_setpoint(ActiveMaze.Checkpoints[0].S)

                # Calculate control signal using the PID controller.
                PID_Output = PID_Controller1.update(ActiveMaze.Ball.S, FrameTimeStep)
                Saturation = PID_Controller1.Saturation # For display.
                ControlSignal = PID_Output[0]
            ''' PID CONTROL END'''
            # Make sure you deal with the cases where no control signal is generated when Active == False.
            ''' MOTOR CONTROL START'''
            # Change the servo motors' angles.
            motor_angle(ControlSignal)
            ''' MOTOR CONTROL END '''

            # Convert control signal into actual Theta (based on measurements).
            Theta = ControlSignal * np.array([3 / 20, 0.1]) # For display. 

        if GraphicsOn == True:
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
            2 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[1][0]), degrees(PID_Output[1][1])), # P.
            3 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[2][0]), degrees(PID_Output[2][1])), # I.
            4 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[2][0]), degrees(PID_Output[2][1])), # D.
            5 : "( {!s:^5} , {!s:^5} )".format(Saturation[0], Saturation[1]), # Saturation.
            6 : "( {0:.1f} , {1:.1f} )".format(degrees(ControlSignal[0]), degrees(ControlSignal[1])), # Control signal.
            7 : "( {0:.1f} , {1:.1f} )".format(degrees(Theta[0]), degrees(Theta[1])) # Theta.
            }
            # Update text sprites with new values.
            Values = ActiveSprites.get_sprites_from_layer(2) # List of value text sprites.
            for Key in OutputValues:
                Values[Key].update(OutputValues[Key])

            # Update changed areas.
            Rects = ActiveSprites.draw(Screen, Background)
            pygame.display.update(Rects)
            ''' PYGAME GRAPHICS END '''

        ''' PYGAME EVENT HANDLER START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0
        ''' PYGAME EVENT HANDLER END '''

        # Enable below to print the timestep of a full loop.
        #CurrentTime = time.perf_counter()
        #TimeStep = CurrentTime - LastTime
        #LastTime = CurrentTime
        #print("{:.0f}ms".format(TimeStep * 1000))

    pygame.quit()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
