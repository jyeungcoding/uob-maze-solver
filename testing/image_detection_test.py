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

# Import classes, functions and values.
from objects import Maze, Ball
from image_detection.image_detection import Image_Detector
from graphics.objects import SpriteBall
from graphics.graphics import initialise_walls, initialise_holes, initialise_checkpoints
from settings import ControlPeriod, PixelScale, White, Black

def image_detection_test():

    # Start clock for time-steps.
    CurrentTime = time.perf_counter() # time.perf_counter() is more accurate but takes more processing time.

    # Initialise image detector.
    Cap = cv2.VideoCapture(0)
    #Cap.set(cv2.CAP_PROP_FPS, 10)
    ImageDetector = Image_Detector(CurrentTime)
    # Capture inital maze elements and ball position.
    ActiveMaze = ImageDetector.initialise_maze()

    # Check MazeModel is correct type.
    if type(ActiveMaze) != Maze:
        raise TypeError("'initialise_maze' should return an object of Maze class. See 'objects.py'.")

    ''' PYGAME GRAPHICS START '''
    # Initialise PyGame.
    pygame.init()
    # Initialise clock.
    Clock = pygame.time.Clock()
    # Initialise display surface.
    Screen = pygame.display.set_mode((ActiveMaze.Size[0] * PixelScale, (ActiveMaze.Size[1] + 22) * PixelScale))
    pygame.display.set_caption("Maze Display")

    # Initialise text module.
    pygame.font.init()
    # Create fonts.
    Font1 = pygame.font.SysFont("Times New Roman", 7 * PixelScale)

    # Generate graphic objects.
    # Generate ball.
    BallList = pygame.sprite.Group()
    SpriteBall1 = SpriteBall(
        ActiveMaze.Ball.S, # [mm], numpy vector, size 2.
        ActiveMaze.Ball.R, # [mm], numpy vector, size 2.
    )
    BallList.add(SpriteBall1)
    # Generate walls.
    WallList = initialise_walls(ActiveMaze.Walls)
    # Generate holes.
    HoleList = initialise_holes(ActiveMaze.Holes)
    # Generate checkpoints.
    CheckpointList = initialise_checkpoints(ActiveMaze.Checkpoints)
    ''' PYGAME GRAPHICS END '''

    # Start main code.
    Running = 1
    while Running == 1:

        # Update clock, limit
        LastTime = CurrentTime
        CurrentTime = time.perf_counter()
        TimeStep = CurrentTime - LastTime # For measuring loop time.
        if CurrentTime - LastTime < ControlPeriod:
            time.sleep(ControlPeriod - CurrentTime + LastTime)
            CurrentTime = time.perf_counter()
            TimeStep = CurrentTime - LastTime # For measuring loop time.

        # Enable below to print the timestep of a full loop.
        #print("{:.0f}ms".format(TimeStep * 1000))

        # Update ball position.
        ActiveMaze.Ball.Active, ActiveMaze.Ball.S = ImageDetector.update_ball(Cap, CurrentTime)

        ''' PYGAME GRAPHICS START '''
        # Check for events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = 0

        if ActiveMaze.Ball.Active == True:
            # Update Sprite Ball position.
            SpriteBall1.rect.centerx = ActiveMaze.Ball.S[0] * PixelScale # Ball position in pixels based on center of ball.
            SpriteBall1.rect.centery = ActiveMaze.Ball.S[1] * PixelScale # Ball position in pixels based on center of ball.
        else:
            SpriteBall1.kill()

        # Create surface with text describing the ball's position.
        BallPositionTxt = Font1.render(str(ActiveMaze.Ball), False, Black)

        # Update graphics. Could optimise.
        Screen.fill(White)
        WallList.draw(Screen) # Draw walls.
        HoleList.draw(Screen) # Draw holes.
        CheckpointList.draw(Screen) # Draw checkpoints.
        BallList.draw(Screen) # Draw ball.
        # Blit text to screen.
        Screen.blit(BallPositionTxt, (7 * PixelScale, (ActiveMaze.Size[1] + 6) * PixelScale))
        pygame.display.flip() # Update display.
        ''' PYGAME GRAPHICS END '''

    pygame.quit()

if __name__ == "__main__":
    image_detection_test()
