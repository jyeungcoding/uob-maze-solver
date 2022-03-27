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

# Import classes, functions and values.
from mazes import Maze1, Maze2, Maze3
from objects import Maze
from graphics.graphics import initialise_background, initialise_checkpoints, initialise_ball, initialise_header, initialise_values, initialise_buttons
from control.pid_controller import PID_Controller
from control.timing_controller import TimingController
from motor_control.motor_control import motor_reset, motor_angle
from settings import ControlPeriod, DisplayScale, White, Black, Kp, Ki, Kd, BufferSize, SaturationLimit, MinSignal

def pid_sim():
    # Generate starting maze.
    ActiveMaze = Maze1

    # Check ActiveMaze is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("ActiveMaze should be of class Maze. See 'objects.py'.")
    if len(ActiveMaze.Checkpoints) == 0:
        raise ValueError("No checkpoints found.")

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

    ''' INITIALISE PID CONTROL '''
    # Initialise PID controller object, see control/pid_controller.py for more information.
    PID_Controller1 = PID_Controller(Kp, Ki, Kd, ActiveMaze.Checkpoints[0].S, BufferSize, SaturationLimit, MinSignal)
    ''' INITIALISE PID CONTROL '''

    ''' INITIALISE MOTOR CONTROL '''
    #motor_reset()
    ''' INITIALISE MOTOR CONTROL '''

    # Starting values.
    ControlSignal = np.array([0.0, 0.0])
    Theta = np.array([0.0, 0.0]) # Theta (radians) should be a size 2 vector of floats.
    Saturation = np.array([False, False])
    PID_Output = [np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0]), np.array([0.0, 0.0])]

    # Start control program.
    Running = 1
    # Start clock.
    StartTime = time.perf_counter() # Record start time.
    SimulationTime = StartTime # Initialise SimulationTime
    TimingController_ = TimingController(StartTime) # Start timing controller.
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

        ''' MAZE SIMULATION START '''
        # Calculate simulation loop time-step.
        LastSimulationTime = SimulationTime
        SimulationTime = time.perf_counter()
        TimeStep = SimulationTime - LastSimulationTime

        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))

        # Simulate next step of maze using theta and a given timestep.
        Output = ActiveMaze.next_step(TimeStep, Theta) # Time step given in s.
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

                # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
                while ((ActiveMaze.Checkpoints[0].S[0] - ActiveMaze.Ball.S[0]) ** 2 + (ActiveMaze.Checkpoints[0].S[1] - ActiveMaze.Ball.S[1]) ** 2) ** 0.5 < 2 and len(ActiveMaze.Checkpoints) > 1:
                    ActiveMaze.Checkpoints.pop(0) # Delete current checkpoint.
                    PID_Controller1.new_setpoint(ActiveMaze.Checkpoints[0].S) # Assign new set point.

                # Calculate control signal using the PID controller.
                PID_Output = PID_Controller1.update(ProcessVariable, ControlTimeStep)
                Saturation = PID_Controller1.Saturation # For display.
                ControlSignal = PID_Output[0]

                # Convert control signal into actual Theta (based on measurements).
                Theta = ControlSignal * np.array([3 / 20, 0.1])
            ''' PID CONTROL END'''

            ''' MOTOR CONTROL START'''
            # Change the servo motors' angles.
            #motor_angle(ControlSignal)
            ''' MOTOR CONTROL END '''

        # Generate strings for output values to be displayed.
        DisplayValues = {
        0 : "{0:.1f}".format(time.perf_counter() - StartTime), # Time elapsed.
        1 : "( {0:.1f} , {1:.1f} )".format(ActiveMaze.Ball.S[0], ActiveMaze.Ball.S[1]), # Ball position.
        2 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[1][0]), degrees(PID_Output[1][1])), # P.
        3 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[2][0]), degrees(PID_Output[2][1])), # I.
        4 : "( {0:.1f} , {1:.1f} )".format(degrees(PID_Output[2][0]), degrees(PID_Output[2][1])), # D.
        5 : "( {!s:^5} , {!s:^5} )".format(Saturation[0], Saturation[1]), # Saturation.
        6 : "( {0:.1f} , {1:.1f} )".format(degrees(ControlSignal[0]), degrees(ControlSignal[1])), # Control signal.
        7 : "( {0:.1f} , {1:.1f} )".format(degrees(Theta[0]), degrees(Theta[1])) # Theta.
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
    pid_sim()
