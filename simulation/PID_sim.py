#!/usr/bin/env python3

# Import modules.
import pygame
import numpy as np
import time
from math import pi

# Import classes, functions and values.
from objects import Maze
from graphics.objects import SpriteBall, SpriteSetPoint
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from simulation.objects import SandboxMaze, SimpleMaze
from settings import PixelScale, White, Black, ThetaMax, BufferSize

def PID_sim():
    # Generate starting maze.
    ActiveMaze = SandboxMaze

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("MazeModel should be of class Maze. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise display surface.
    Screen = pygame.display.set_mode((ActiveMaze.Size[0] * PixelScale, (ActiveMaze.Size[1] + 42) * PixelScale))
    pygame.display.set_caption("Maze Simulation")

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
    # PID Coefficients
    Kp = 2.99e-3
    Ki = 1e-4
    Kd = 1e-3

    # Initialise a few variables.
    ProcessVariable = ActiveMaze.Ball.S # Set ProcessVariable as the ball's position.
    SetPoint = ActiveMaze.Checkpoints[0].S # Set SetPoint as the first checkpoint.
    ErrorValue = SetPoint - ProcessVariable # Calculate initial error value.
    ErrorIntegral = np.array([0.0, 0.0]) # Initialise integrator.
    Saturation = np.array([False, False]) # Initialise saturation check.
    LeastSquare = np.zeros((9, BufferSize)) # Initialise LeastSquare error buffer.
    BufferIteration = 0 # Record buffer iteration number.
    ''' INITIALISE PID CONTROL '''

    # Theta (radians) should be a size 2 vector of floats.
    Theta = np.array([0.0, 0.0])

    # Start control program.
    Running = 1
    # Start clock for time-steps.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.
    StartTime = CurrentTime # Record start time, currently unused.
    TimeStep = 0.001 # First timestep: value unimportant, but has to be small and non-zero.
    i = 1
    while Running == 1:

        # Simulate next step of maze using theta and a given timestep.
        Output = ActiveMaze.next_step(TimeStep, Theta) # Time step given in s.

        ''' PID CONTROL START '''
        # Set ProcessVariable as the ball's position.
        ProcessVariable = Output[1]

        # If the ball is within 2mm of the set point, delete the current checkpoint and set the new first checkpoint as the set point.
        while ((SetPoint[0] - ProcessVariable[0]) ** 2 + (SetPoint[1] - ProcessVariable[1]) ** 2) ** 0.5 < 2 and len(ActiveMaze.Checkpoints) > 1:
            ActiveMaze.Checkpoints.pop(0)
            SetPoint = ActiveMaze.Checkpoints[0].S
            ErrorValue = SetPoint - ProcessVariable # Reset error value.
            ErrorIntegral = np.array([0.0, 0.0]) # Reset error integral.
            LeastSquare = np.zeros((9, BufferSize)) # Initialise LeastSquare error buffer.
            BufferIteration = 0 # Reset buffer iteration number.

        # Calculate error value.
        ErrorValue = SetPoint - ProcessVariable

        # Update error buffer.
        LeastSquare[0:3] = np.roll(LeastSquare[0:3], -1, 1)
        LeastSquare[0:3, BufferSize - 1] = TimeStep + LeastSquare[0, BufferSize - 2], ErrorValue[0], ErrorValue[1]
        BufferIteration += 1 # Update buffer iteration number.

        # Conditional integrator, clamps if ControlSignal is saturated and the error is the same sign as the output.
        if Saturation[0] == True and Saturation[1] == True and np.sign(ErrorValue)[0] == np.sign(Theta)[0] and np.sign(ErrorValue)[1] == np.sign(Theta)[1]:
            pass
        elif Saturation[0] == False and Saturation[1] == True and np.sign(ErrorValue)[1] == np.sign(Theta)[1]:
            ErrorIntegral[0] += ErrorValue[0] * TimeStep
        elif Saturation[1] == True and Saturation[0] == False and np.sign(ErrorValue)[0] == np.sign(Theta)[0]:
            ErrorIntegral[1] += ErrorValue[1] * TimeStep
        else:
            ErrorIntegral += ErrorValue * TimeStep

        # Calculate derivative of error value.

        if BufferIteration > 10:
            MeanT = np.mean(LeastSquare[0])
            MeanX = np.mean(LeastSquare[1])
            MeanY = np.mean(LeastSquare[2])
            LeastSquare[3] = tuple(map(lambda T : T - MeanT, LeastSquare[0]))
            LeastSquare[4] = tuple(map(lambda x : x - MeanX, LeastSquare[1]))
            LeastSquare[5] = tuple(map(lambda y : y - MeanY, LeastSquare[2]))
            LeastSquare[6] = tuple(map(lambda T_MeanT, x_MeanX: T_MeanT * x_MeanX, LeastSquare[3], LeastSquare[4]))
            LeastSquare[7] = tuple(map(lambda T_MeanT, y_MeanY: T_MeanT * y_MeanY, LeastSquare[3], LeastSquare[5]))
            LeastSquare[8] = tuple(map(lambda T_MeanT: T_MeanT ** 2, LeastSquare[3]))

            GradX = np.sum(LeastSquare[6]) / np.sum(LeastSquare[8])
            GradY = np.sum(LeastSquare[7]) / np.sum(LeastSquare[8])
            ErrorDerivative = np.array([GradX, GradY])
        else:
            ErrorDerivative = np.array([0.0, 0.0])

        # Calculate PID Terms.
        ProportionalTerm = Kp * ErrorValue
        IntegralTerm = Ki * ErrorIntegral
        DerivativeTerm = Kd * ErrorDerivative
        # Calculate ControlSignal with PID equation.
        ControlSignal = ProportionalTerm + IntegralTerm + DerivativeTerm

        # Saturation clamp.
        Theta = ControlSignal
        Saturation = np.array([False, False])
        if Theta[0] > ThetaMax: # If Theta exceeds ThetaMax clamp the integrator and output ThetaMax.
            Theta[0] = ThetaMax
            Saturation[0] = True
        elif Theta[0] < -ThetaMax:
            Theta[0] = -ThetaMax
            Saturation[0] = True
        if Theta[1] > ThetaMax:
            Theta[1] = ThetaMax
            Saturation[1] = True
        elif Theta[1] < -ThetaMax:
            Theta[1] = -ThetaMax
            Saturation[1] = True

        # Impose sanity check on Theta, raise error if greater than 0.25pi.
        if Theta[0] > ThetaMax or Theta[0] < -ThetaMax or Theta[1] > ThetaMax or Theta[1] < -ThetaMax:
            raise Exception("Control signal exceeded 0.25*pi in one or both axes. PLease check PID settings.")
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
        PIDTermsTxt = Font1.render("P: %s, I: %s, D: %s" % (np.round(ProportionalTerm * 360 / (2 * pi), 1), np.round(IntegralTerm * 360 / (2 * pi), 1), np.round(DerivativeTerm * 360 / (2 * pi), 1)), False, Black)
        # Create surface with text displaying the control signal in degrees.
        ControlSignalTxt = Font1.render("Saturation: %s, Control Signal: %s, Theta: %s" % (Saturation, np.round(ControlSignal * 360 / (2 * pi), 1), np.round(Theta * 360 / (2 * pi), 1)), False, Black)

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
