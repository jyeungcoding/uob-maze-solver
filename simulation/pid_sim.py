#!/usr/bin/env python3
'''
This file contains PID_sim() which simulates PID control of the maze using the PID
controller in control/pid_controller.py. 
'''

# Import modules.
import pygame
import numpy as np
import time
from math import pi

# Import classes, functions and values.
from objects import Maze
from graphics.objects import SpriteBall, SpriteSetPoint
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from simulation.objects import SandboxMaze, SimpleMaze, CircleMaze
from control.pid_controller import PID_Controller
from settings import PixelScale, White, Black, Kp, Ki, Kd, BufferSize, SaturationLimit

def PID_sim():
    # Generate starting maze.
    ActiveMaze = SimpleMaze

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("MazeModel should be of class Maze. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise display surface.
    Screen = pygame.display.set_mode((ActiveMaze.Size[0] * PixelScale, (ActiveMaze.Size[1] + 42) * PixelScale))
    pygame.display.set_caption("PID Simulation")

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
    PID_Controller1 = PID_Controller(Kp, Ki, Kd, ActiveMaze.Checkpoints[0].S, BufferSize, SaturationLimit)
    ''' INITIALISE PID CONTROL '''

    # Theta (radians) should be a size 2 vector of floats.
    Theta = np.array([0.0, 0.0])

    # Start control program.
    Running = 1
    # Start clock for time-steps.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.
    StartTime = CurrentTime # Record start time, currently unused.
    TimeStep = 0
    while Running == 1:

        # Simulate next step of maze using theta and a given timestep.
        Output = ActiveMaze.next_step(TimeStep, Theta) # Time step given in s.

        ''' PID CONTROL START '''
        if Output[0] == True:
            # Set ProcessVariable as the ball's position.
            ProcessVariable = Output[1]

            # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
            while ((ActiveMaze.Checkpoints[0].S[0] - ProcessVariable[0]) ** 2 + (ActiveMaze.Checkpoints[0].S[1] - ProcessVariable[1]) ** 2) ** 0.5 < 2 and len(ActiveMaze.Checkpoints) > 1:
                ActiveMaze.Checkpoints.pop(0)
                PID_Controller1.new_setpoint(ActiveMaze.Checkpoints[0].S)

            # Calculate control signal using the PID controller.
            PID_Output = PID_Controller1.update(ProcessVariable, TimeStep)
            Theta = PID_Output[0]

            # Theta sanity check: raise error if greater than 0.25pi.
            if Theta[0] > SaturationLimit or Theta[0] < -SaturationLimit or Theta[1] > SaturationLimit or Theta[1] < -SaturationLimit:
                raise Exception("Control signal exceeded SaturationLimit in one or both axes. PLease check PID settings.")
        ''' PID CONTROL END'''

        ''' PYGAME GRAPHICS START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0

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
        ControlSignalTxt = Font1.render("Saturation: %s, Control Signal: %s" % (PID_Controller1.Saturation, np.round(Theta * 360 / (2 * pi), 1)), False, Black)

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

        # Calculate time elapsed in simulation loop.
        LastTime = CurrentTime
        CurrentTime = time.perf_counter()
        TimeStep = CurrentTime - LastTime
        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))

    pygame.quit()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
