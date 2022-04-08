#!/usr/bin/env python3
'''
This file contains object classes required for maze control and simulation.
'''

# Import modules.
import numpy as np
from math import sin
import random

# Import functions and values.
from settings import FrameSize, FrameHorizontal, FrameVertical, FrameBounce, WallBounce, BallRadius, BallMass, HoleRadius, Drag, ImageNoise

class Ball():
    # Class for the metal ball.
    def __init__(self, Position, Velocity = np.array([0, 0])):
        # Position and velocity should be provided in a numpy vector, Size 2.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")
        if type(Velocity) != np.ndarray:
            raise TypeError("Velocity should be given in a size 2 numpy array.")
        elif Velocity.shape != (2,):
            raise ValueError("Velocity should be given in a size 2 numpy array.")

        self.Active = True # True while ball is on maze.
        self.S = Position # [mm], Position taken as centre of ball.
        self.v = Velocity # [mm/s]
        self.a = np.array([0, 0]) # [mm/s^2]
        self.R = BallRadius # [mm]
        self.Mass = BallMass # [kg] (Currently unused.)
        self.Drag = Drag # See settings.

        # Saves balls's last position, needed for collision detection
        self.LastS = self.S
        self.LastPositionLeft = self.S[0] - self.R
        self.LastPositionRight = self.S[0] + self.R
        self.LastPositionTop = self.S[1] - self.R
        self.LastPositionBottom = self.S[1] + self.R

    def __repr__(self):
        # Makes the class printable.
        return "Ball(Active: %s, Position: %s, Velocity: %s, Acceleration: %s)" % (self.Active, np.round(self.S, 1), np.round(self.v, 1), np.round(self.a, 1))

    def last_position(self):
        # Saves balls's last position, needed for collision detection.
        self.LastS = self.S
        self.LastPositionLeft = self.S[0] - self.R
        self.LastPositionRight = self.S[0] + self.R
        self.LastPositionTop = self.S[1] - self.R
        self.LastPositionBottom = self.S[1] + self.R

    def next_a(self, Theta):
        # NewA[mm/s^2] = gsin(theta)*1000
        NewA = 9.81 * np.sin(Theta) * 1000
        # Artificial drag on ball: approximates air resistance and friction.
        NewA -= self.Drag * np.sign(self.v) * (4 / (abs(0.005 * self.v) + 0.5)) + 0.02 * self.v
        return NewA

    def next_v(self, TimeStep, NewA):
        # Calculate next v.
        NewV = self.v + (self.a + NewA) * TimeStep / 2
        # Stop ball if v is too small.
        if NewV[0] < 0.05 and NewV[0] > -0.05:
            NewV[0] = 0.0
        if NewV[1] < 0.05 and NewV[1] > -0.05:
            NewV[1] = 0.0
        return NewV

    def next_S(self, TimeStep, NewV):
        # Calculate next S.
        NewS = self.S + (self.v + NewV) * TimeStep / 2
        return NewS

    def position_values(self):
        # Sets useful position values for collision detection.
        self.Left = self.S[0] - self.R # [mm], float
        self.Right = self.S[0] + self.R # [mm], float
        self.Top = self.S[1] - self.R # [mm], float
        self.Bottom = self.S[1] + self.R # [mm], float

    def corner_reflection(self, m, Bounce):
        # Handles corner reflections. Velocity reflection is reliable, position reflection is inaccurate but acceptable.
        ReflectMatrix = (1 / (1 + m ** 2)) * np.array([[m ** 2 - 1, - 2 * m], [- 2 * m, 1 - m ** 2]]) # Matrix for reflection in y = mx, followed by an inverse.

        # Position reflection based on tangent to impact. IMPROVEMENT: USE RADIAL TO CATESIAN CONVERSION (sin(theta), cos(theta))
        dS = self.S - self.LastS
        dS[1] = - dS[1] # Required as our y axis goes from up to down.
        np.transpose(dS) # Required as we use size (2, 1) arrays instead of (1, 2) arrays for simplicity.
        dS = ReflectMatrix.dot(dS)
        np.transpose(dS) # Required as we use size (2, 1) arrays instead of (1, 2) arrays for simplicity.
        dS[1] = - dS[1] # Required as our y axis goes from up to down.
        self.S = self.S + 4 * dS # dS multiplied by 4 to stop ball from "falling" into the wall.

        # Velocity reflection based on tangent to impact.
        self.v[1] = -self.v[1] # Required as our y axis goes from up to down.
        np.transpose(self.v) # Required as we use size (2, 1) arrays instead of (1, 2) arrays for simplicity.
        self.v = ReflectMatrix.dot(self.v)
        np.transpose(self.v) # Required as we use size (2, 1) arrays instead of (1, 2) arrays for simplicity.
        self.v[1] = -self.v[1] # Required as we use size (2, 1) arrays instead of (1, 2) arrays for simplicity.
        self.v = Bounce * self.v

    def wall_collision(self, Walls):
        # Handles wall collision in 8 cases.
        self.position_values() # Update position values of ball.
        for wall in Walls:
            if self.Left <= wall.Right and self.LastPositionLeft > wall.Right \
                    and self.LastS[1] >= wall.Top and self.LastS[1] <= wall.Bottom: # For right side "flat" reflection.
                self.S[0] = wall.S[0] + wall.Size[0] + wall.S[0] + wall.Size[0] - self.S[0] + self.R + self.R
                self.v[0] = - wall.Bounce * self.v[0]
            elif self.Right >= wall.Left and self.LastPositionRight < wall.Left \
                    and self.LastS[1] >= wall.Top and self.LastS[1] <= wall.Bottom: # For left side "flat" reflection.
                self.S[0] = wall.S[0] + wall.S[0] - self.S[0] - self.R - self.R
                self.v[0] = - wall.Bounce * self.v[0]
            elif self.Top <= wall.Bottom and self.LastPositionTop > wall.Bottom \
                    and self.LastS[0] >= wall.Left and self.LastS[0] <= wall.Right: # For bottom side "flat" reflection.
                self.S[1] = wall.S[1] + wall.Size[1] + wall.S[1] + wall.Size[1] - self.S[1] + self.R + self.R
                self.v[1] = - wall.Bounce * self.v[1]
            elif self.Bottom >= wall.Top and self.LastPositionBottom < wall.Top \
                    and self.LastS[0] >= wall.Left and self.LastS[0] <= wall.Right: # For top side "flat" reflection.
                self.S[1] = wall.S[1] + wall.S[1] - self.S[1] - self.R - self.R
                self.v[1] = - wall.Bounce * self.v[1]
            elif self.R > ((self.S[0] - wall.Left) ** 2 + (self.S[1] - wall.Top) ** 2 ) ** 0.5 \
                    and self.R <= ((self.LastS[0] - wall.Left) ** 2 + (self.LastS[1] - wall.Top) ** 2 ) ** 0.5: # Top left corner collision.
                y = wall.Top - self.S[1] # Inversed as our y axis runs from up to down.
                x = self.S[0] - wall.Left
                m = y / x # Calculate y = mx of tangent to impact.
                self.corner_reflection(m, wall.Bounce)
            elif self.R > ((self.S[0] - wall.Right) ** 2 + (self.S[1] - wall.Top) ** 2 ) ** 0.5 \
                    and self.R <= ((self.LastS[0] - wall.Right) ** 2 + (self.LastS[1] - wall.Top) ** 2 ) ** 0.5: # Top right corner collision.
                y = wall.Top - self.S[1]
                x = self.S[0] - wall.Right
                m = y / x
                self.corner_reflection(m, wall.Bounce)
            elif self.R > ((self.S[0] - wall.Left) ** 2 + (self.S[1] - wall.Bottom) ** 2 ) ** 0.5 \
                    and self.R <= ((self.LastS[0] - wall.Left) ** 2 + (self.LastS[1] - wall.Bottom) ** 2 ) ** 0.5: # Bottom left corner collision.
                y = wall.Bottom - self.S[1]
                x = self.S[0] - wall.Left
                m = y / x
                self.corner_reflection(m, wall.Bounce)
            elif self.R > ((self.S[0] - wall.Right) ** 2 + (self.S[1] - wall.Bottom) ** 2 ) ** 0.5 \
                    and self.R <= ((self.LastS[0] - wall.Right) ** 2 + (self.LastS[1] - wall.Bottom) ** 2 ) ** 0.5: # Bottom right corner collision.
                y = wall.Bottom - self.S[1]
                x = self.S[0] - wall.Right
                m = y / x
                self.corner_reflection(m, wall.Bounce)

    def hole_collision(self, Holes):
        # Handles collisions with holes. Set ball as not Active if it falls in.
        for hole in Holes:
            if hole.R + 1 > ((hole.S[0] - self.S[0]) ** 2 + (hole.S[1] - self.S[1]) ** 2 ) ** 0.5:
                self.Active = False

    def next_step(self, TimeStep, Theta, Walls, Holes):
        # Calculate next ball position based on model.
        if self.Active == True:
            self.last_position() # Save last position of ball.

            # Process motion.
            self.a = self.next_a(Theta)
            self.v = self.next_v(TimeStep, self.a)
            self.S = self.next_S(TimeStep, self.v)

            # Process collisions.
            self.wall_collision(Walls)
            self.hole_collision(Holes)

class Wall():
    # Class for walls.
    def __init__(self, Position, Size, Bounce = WallBounce):
        # Position and Size should be provided in numpy vectors, Size 2.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")
        elif type(Size) != np.ndarray:
            raise TypeError("Size should be given in a size 2 numpy array.")
        elif Size.shape != (2,):
            raise ValueError("Size should be given in a size 2 numpy array.")

        self.S = Position # [mm] Postiion taken from top left corner.
        self.Size = Size # [mm]
        self.Bounce = Bounce # Coefficient of reflectivity off walls. Positive float.

        # Useful position values for collision detection.
        self.Left = self.S[0] # [mm], float
        self.Right = self.S[0] + self.Size[0] # [mm], float
        self.Top = self.S[1] # [mm], float
        self.Bottom = self.S[1] + self.Size[1] # [mm], float

    def __repr__(self):
        # Makes the class printable.
        return "Wall(Position: %s, Size: %s)" % (np.round(self.S, 1), np.round(self.Size, 1))

class Hole():
    # Class for holes.
    def __init__(self, Position):
        # Position and Size should be provided in numpy vectors, Size 2.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        self.S = Position # [mm]
        self.R = HoleRadius # [mm]

    def __repr__(self):
        # Makes the class printable.
        return "Hole(Position: %s)" % (np.round(self.S, 1))

class Checkpoint():
    # Class for checkpoints.
    def __init__(self, Position, Special = False, Radius = None, Time = None, HardControlSignal = None):
        # Position and Size should be provided in numpy vectors, Size 2.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        self.S = Position # [mm]
        self.Special = Special # Set to true if there are optional args.
        self.Radius = Radius # Custom radius.
        self.Time = Time # Custom time to "pass".
        self.HardControlSignal = HardControlSignal # Custom control signal output.

    def __repr__(self):
        # Printable.
        return "Checkpoint(Position: %s, Special: %s)" % (np.round(self.S, 1), self.Special)

class Maze():
    # Class for full model of maze.
    def __init__(self, ball, walls, holes, checkpoints):
        # Check if maze has been initialised correctly.
        if type(ball) != Ball:
            raise TypeError("Ball should be of Ball class. Check 'objects.py' for more information. ")
        elif type(walls) != list:
            raise TypeError("Walls should be given in a list.")
        elif type(holes) != list:
            raise TypeError("Holes should be given in a list.")
        elif type(checkpoints) != list:
            raise TypeError("Checkpoints should be given in a list.")

        for wall in walls:
            if type(wall) != Wall:
                raise TypeError("Wall should be of Wall class. Check 'objects.py' for more information. ")
        for hole in holes:
            if type(hole) != Hole:
                raise TypeError("Hole should be of Hole class. Check 'objects.py' for more information. ")
        for checkpoint in checkpoints:
            if type(checkpoint) != Checkpoint:
                raise TypeError("Checkpoint should be of Checkpoint class. Check 'objects.py' for more information. ")

        self.Size = FrameSize # Size of frame, see settings.
        self.Ball = ball
        self.Walls = walls # Should be given in list.
        self.Holes = holes # Should be given in list.
        self.Checkpoints = checkpoints # Should be given in list. Checkpoint order matters!

        # Generate frame.
        Frame = [
            Wall(
                np.array([0, 0]), # Standard units (see settings).
                np.array([FrameVertical, FrameSize[1]]), # Standard units (see settings).
                FrameBounce
            ),
            Wall(
                np.array([FrameSize[0] - FrameVertical + 1, 0]),
                np.array([FrameVertical, FrameSize[1]]),
                FrameBounce
            ),
            Wall(
                np.array([0, 0]),
                np.array([FrameSize[0], FrameHorizontal]),
                FrameBounce
            ),
            Wall(
                np.array([0, FrameSize[1] - FrameHorizontal + 1]),
                np.array([FrameSize[0], FrameHorizontal]),
                FrameBounce
            )
        ]
        # Add frame to maze.
        self.Walls.extend(Frame)

    def __repr__(self):
        # Makes the class printable.
        return "Maze(Size: %s, Ball: %s, Walls: %s, Holes: %s, Checkpoints: %s)" % (np.round(self.Size, 1), self.Ball, self.Walls, self.Holes, self.Checkpoints)

    def image_noise(self):
        # Simulate random noise from image detection.
        BallPosition = self.Ball.S + np.array([random.randint(-ImageNoise, ImageNoise), random.randint(-ImageNoise, ImageNoise)])
        return BallPosition

    def next_step(self, TimeStep, Theta = np.array([0.0, 0.0])):
        # Calculate next ball position based on model, output info.
        self.Ball.next_step(TimeStep, Theta, self.Walls, self.Holes)
        BallPosition = self.image_noise()
        return self.Ball.Active, BallPosition

if __name__ == "__main__":
    import doctest
    doctest.testmod()
