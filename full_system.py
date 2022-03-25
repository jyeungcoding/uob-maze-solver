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
from math import pi

# Import classes, functions and values.
from objects import Maze
from graphics.objects import SpriteBall, SpriteSetPoint
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from image_detection.image_detection import Image_Detector
from control.pid_controller import PID_Controller
from motor_control.motor_control import motor_reset, motor_angle
from settings import ControlPeriod, GraphicsPeriod, PixelScale, White, Black, Kp, Ki, Kd, BufferSize, SaturationLimit, MinSignal

def full_system():

    # Start clock.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.
    StartTime = CurrentTime # Record start time, currently unused.
    LastTime = CurrentTime # For timing each full loop.
    LastFrameTime = CurrentTime # For timing each image frame loop.

    ''' IMAGE DETECTION START '''
    # Initialise image detector.
    Cap = cv2.VideoCapture(0)
    #self.cap.set(cv2.CAP_PROP_FPS, 10)
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
    Screen = pygame.display.set_mode((ActiveMaze.Size[0] * PixelScale, (ActiveMaze.Size[1] + 42) * PixelScale))
    pygame.display.set_caption("System Display")

    # Initialise text module.
    pygame.font.init()
    # Create fonts.
    Font1 = pygame.font.SysFont("Times New Roman", 7 * PixelScale)

    # Generate graphic objects.
    BallList = pygame.sprite.Group() # Generate ball.
    SpriteBall1 = SpriteBall(
        ActiveMaze.Ball.S, # [mm], numpy vector, size 2.
        ActiveMaze.Ball.R, # [mm], numpy vector, size 2.
    )
    BallList.add(SpriteBall1)
    WallList = initialise_walls(ActiveMaze.Walls) # Generate walls.
    HoleList = initialise_holes(ActiveMaze.Holes) # Generate holes.
    CheckpointList = initialise_checkpoints(ActiveMaze.Checkpoints) # Generate checkpoints.

    # Set the first SpriteCheckpoint as the SpriteSetPoint and remove it from CheckpointList so it isn't drawn twice.
    CheckpointIter1 = iter(CheckpointList) # Sprite groups aren't indexed, so it is necessary to create an iterable.
    CheckpointIter2 = iter(CheckpointList)
    SpriteSetPoint1 = SpriteSetPoint(next(CheckpointIter1).S) # Set point is drawn red instead of blue.
    next(CheckpointIter2).kill()
    ''' PYGAME GRAPHICS END '''

    ''' INITIALISE PID CONTROL '''
    # Initialise PID controller object, see control/pid_controller.py for more information.
    PID_Controller1 = PID_Controller(Kp, Ki, Kd, ActiveMaze.Checkpoints[0].S, BufferSize, SaturationLimit, MinSignal)
    ''' INITIALISE PID CONTROL '''

    ''' INITIALISE MOTOR CONTROL '''
    #motor_reset()
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
                ControlSignal = PID_Output[0]
            ''' PID CONTROL END'''
            # Make sure you deal with the cases where no control signal is generated when Active == False.
            ''' MOTOR CONTROL START'''
            # Change the servo motors' angles.
            motor_angle(ControlSignal)
            ''' MOTOR CONTROL END '''

        if GraphicsOn == True:
            ''' PYGAME GRAPHICS START '''
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
            # Create surface with text describing the PID Terms.
            PIDTermsTxt = Font1.render("P: %s, I: %s, D: %s" % (np.round(PID_Output[1] * 360 / (2 * pi), 1), np.round(PID_Output[2] * 360 / (2 * pi), 1), np.round(PID_Output[3] * 360 / (2 * pi), 1)), False, Black)
            # Create surface with text displaying the control signal in degrees.
            ControlSignalTxt = Font1.render("Saturation: %s, Control Signal: %s" % (PID_Controller1.Saturation, np.round(ControlSignal * 360 / (2 * pi), 1)), False, Black)

            # Update graphics. Could optimise.
            Screen.fill(White)
            WallList.draw(Screen) # Draw walls.
            HoleList.draw(Screen) # Draw holes.
            CheckpointList.draw(Screen) # Draw checkpoints.
            Screen.blit(SpriteSetPoint1.image, SpriteSetPoint1.rect) # Draw set point.
            BallList.draw(Screen) # Draw ball.
            # Blit text to screen.
            Screen.blit(BallPositionTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 6) * PixelScale))
            Screen.blit(PIDTermsTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 17) * PixelScale))
            Screen.blit(ControlSignalTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 28) * PixelScale))

            pygame.display.flip() # Update display.
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
