#!/usr/bin/env python3

# Import modules.
import numpy as np
import time
from math import pi

# Import classes, functions and values.
from objects import Maze, Hole, Checkpoint
from graphics.objects import SpriteBall, SpriteSetPoint
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from simulation.tilt_maze import tilt_maze
from simulation.default_objects import Frame, DefaultMaze
from settings import PixelScale, White

MazeModel = DefaultMaze

# Add frame to MazeModel.
MazeModel.Walls.extend(Frame)

Hole1 = Hole(np.array([200, 200]))
MazeModel.Holes.append(Hole1)
Checkpoint1 = Checkpoint(np.array([200, 160]))
MazeModel.Checkpoints.append(Checkpoint1)

def main_control(Mode, Graphics):

    # Check MazeModel is correct type.
    if type(MazeModel) != Maze:
        raise TypeError("MazeModel should be of class Maze. See 'objects.py'")

    ''' PYGAME GRAPHICS START '''
    if Graphics == 1:
        # Import graphics module.
        import pygame
        # Initialise PyGame.
        pygame.init()
        # Initialise clock.
        Clock = pygame.time.Clock()
        # Initialise display surface.
        Screen = pygame.display.set_mode([MazeModel.Size[0] * PixelScale, MazeModel.Size[1] * PixelScale])
        pygame.display.set_caption('Maze Simulation')

        # Generate ball.
        BallList = pygame.sprite.Group()
        SpriteBall1 = SpriteBall(
            MazeModel.Ball.S, # [mm], numpy vector, size 2.
            MazeModel.Ball.R, # [mm], numpy vector, size 2.
        )
        BallList.add(SpriteBall1)
        # Generate walls.
        WallList = initialise_walls(MazeModel.Walls)
        # Generate holes.
        HoleList = initialise_holes(MazeModel.Holes)
        # Generate checkpoints.
        CheckpointList = initialise_checkpoints(MazeModel.Checkpoints)
    ''' PYGAME GRAPHICS END '''

    # Start program.
    ''' PID CONTROL START '''
    Running = 1

    Kp = 0.5
    Ki = 0
    Kd = 0.1

    Integral = np.array([0.0, 0.0])

    ErrorValue = np.array([0.0, 0.0])

    ''' PID CONTROL END '''

    # Theta (radians) should be a size 2 vector of floats.
    Theta = np.array([0.0, 0.0])

    # Start clock for time-steps.
    CurrentTime = time.perf_counter()
    StartTime = CurrentTime

    while Running == 1:

        # Update maze, see objects.py.
        LastTime = CurrentTime
        CurrentTime = time.perf_counter()
        TimeStep = CurrentTime - LastTime

        MazeModel.update(TimeStep, Theta) # Time step given in s.

        ''' PID CONTROL START'''
        if Mode == 1 and MazeModel.Ball.Active == True:
            ProcessVariable = MazeModel.Ball.S

            SetPoint = MazeModel.Checkpoints[0].S

            LastErrorValue = ErrorValue

            ErrorValue = SetPoint - ProcessVariable

            Integral += ErrorValue

            IntegralValue = Integral / (CurrentTime - StartTime)

            DerivativeValue = (ErrorValue - LastErrorValue) / TimeStep

            Theta = Kp * ErrorValue + Ki * IntegralValue + Kd * DerivativeValue

            if Theta[0] > 0.5 * pi:
                Theta[0] = 0.5 * pi
            elif Theta[0] < -0.5 * pi:
                Theta[0] = -0.5 * pi
            if Theta[1] > 0.5 * pi:
                Theta[1] = 0.5 * pi
            elif Theta[1] < -0.5 * pi:
                Theta[1] = -0.5 * pi
        ''' PID CONTROL END'''

        ''' PYGAME CONTROLS START '''
        if Graphics == 1:
            # Check for events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Running = 0
                elif (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and Mode == 0:
                    # Manual maze tilt.
                    Theta = tilt_maze(event, Theta)
            ''' PYGAME CONTROLS END '''

            ''' PYGAME GRAPHICS START '''
            if MazeModel.Ball.Active == True:
                # Update Sprite Ball position.
                SpriteBall1.rect.centerx = MazeModel.Ball.S[0] * PixelScale # Ball position in pixels based on center of ball.
                SpriteBall1.rect.centery = MazeModel.Ball.S[1] * PixelScale # Ball position in pixels based on center of ball.
            else:
                SpriteBall1.kill()

            if Mode == 1:
                CurrentCheckpoint1 = SpriteSetPoint(SetPoint)

            # Update graphics. Could optimise.
            Screen.fill(White)
            WallList.draw(Screen) # Draw walls.
            HoleList.draw(Screen) # Draw holes.
            CheckpointList.draw(Screen) # Draw checkpoints.
            if Mode == 1:
                Screen.blit(CurrentCheckpoint1.image, CurrentCheckpoint1.rect)
            BallList.draw(Screen) # Draw ball.
            pygame.display.flip() # Update display.

            Clock.tick()
            # Enable below to print T or fps of full graphics loop.
            #print("{:.0f}ms".format(Clock.get_time()))
            #print("{:.0f}fps".format(1/Clock.get_time()*1000))

    if Graphics == 1:
        pygame.quit()
    ''' PYGAME GRAPHICS END '''

def main():
    main_control(0, 1)

if __name__ == "__main__":
    main()
