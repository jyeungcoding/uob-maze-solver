#!/usr/bin/env python3
'''
This file contains object classes required for maze control and simulation.
'''

# Import modules.
import numpy as np
from math import sin

# Import values.
from settings import Bounce, BallRadius, BallMass, HoleRadius, Drag

class Ball():
    # Class for the metal ball.
    def __init__(self, Position, Velocity = 0, Acceleration = 0):
        # Position, velocity and acceleration should be provided in a numpy vector, Size 2.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")
        if type(Velocity) != np.ndarray:
            raise TypeError("Velocity should be given in a size 2 numpy array.")
        elif Velocity.shape != (2,):
            raise ValueError("Velocity should be given in a size 2 numpy array.")
        if type(Acceleration) != np.ndarray:
            raise TypeError("Acceleration should be given in a size 2 numpy array.")
        elif Acceleration.shape != (2,):
            raise ValueError("Acceleration should be given in a size 2 numpy array.")

        self.Active = True # True while ball is on maze.
        self.S = Position # [mm], Position taken as centre of ball.
        self.v = Velocity # [mm/s]
        self.a = Acceleration # [mm/s^2]
        self.R = BallRadius # [mm]
        self.Mass = BallMass # [kg] (Currently unused.)
        self.Drag = Drag # See settings.

        # Saves balls's last position, needed for collision detection
        self.LastPositionLeft = self.S[0] - self.R
        self.LastPositionRight = self.S[0] + self.R
        self.LastPositionTop = self.S[1] - self.R
        self.LastPositionBottom = self.S[1] + self.R

    def __repr__(self):
        # Printable.
        return "Ball(Active: %s, Position: %s, Velocity: %s, Acceleration: %s)" % (self.Active, self.S, self.v, self.a)

    def last_position(self):
        # Saves balls's last position, needed for collision detection.
        self.LastPositionLeft = self.S[0] - self.R
        self.LastPositionRight = self.S[0] + self.R
        self.LastPositionTop = self.S[1] - self.R
        self.LastPositionBottom = self.S[1] + self.R

    def next_a(self, Theta):
        # NewA[mm/s^2] = gsin(theta)*1000
        NewA = 9.81 * np.sin(Theta) * 1000
        # Artificial drag on ball: approximates air resistance and friction.
        NewA -= self.Drag * self.v
        return NewA

    def next_v(self, TimeStep, NewA):
        NewV = self.v + (self.a + NewA) * TimeStep / 2
        return NewV

    def next_S(self, TimeStep, NewV):
        NewS = self.S + (self.v + NewV) * TimeStep / 2
        return NewS

    def wall_collision(self, Walls):
        for wall in Walls:
            if self.S[0] - self.R < wall.S[0] + wall.Size[0] and self.LastPositionLeft >= wall.S[0] + wall.Size[0]:
                self.S[0] = wall.S[0] + wall.Size[0] + wall.S[0] + wall.Size[0] - self.S[0] + self.R + self.R
                self.v[0] = - Bounce * self.v[0]
            elif self.S[0] + self.R > wall.S[0] and self.LastPositionRight <= wall.S[0]:
                self.S[0] = wall.S[0] + wall.S[0] - self.S[0] - self.R - self.R
                self.v[0] = - Bounce * self.v[0]
            if self.S[1] - self.R < wall.S[1] + wall.Size[1] and self.LastPositionTop >= wall.S[1] + wall.Size[1]:
                self.S[1] = wall.S[1] + wall.Size[1] + wall.S[1] + wall.Size[1] - self.S[1] + self.R + self.R
                self.v[1] = - Bounce * self.v[1]
            elif self.S[1] + self.R > wall.S[1] and self.LastPositionBottom <= wall.S[1]:
                self.S[1] = wall.S[1] + wall.S[1] - self.S[1] - self.R - self.R
                self.v[1] = - Bounce * self.v[1]

    def hole_collision(self, Holes):
        for hole in Holes:
            if hole.R + 1 > ((hole.S[0] - self.S[0]) ** 2 + (hole.S[1] - self.S[1]) ** 2 ) ** 0.5:
                self.Active = False

    def update(self, TimeStep, Theta, Walls, Holes):
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
    def __init__(self, Position, Size):
        # Position and Size should be provided in numpy vectors, Size 2.
        self.S = Position # [mm] Postiion taken from top left corner.
        self.Size = Size # [mm]

    def __repr__(self):
        # Printable.
        return "Wall(Position: %s, Size: %s)" % (self.S, self.Size)

class Hole():
    # Class for holes.
    def __init__(self, Position):
        # Position and Size should be provided in numpy vectors, Size 2.
        self.S = Position # [mm]
        self.R = HoleRadius # [mm]

    def __repr__(self):
        # Printable.
        return "Hole(Position: %s)" % (self.S)

class Checkpoint():
    # Class for checkpoints.
    def __init__(self, Position):
        # Position and Size should be provided in numpy vectors, Size 2.
        self.S = Position # [mm]

    def __repr__(self):
        # Printable.
        return "Checkpoint(Position: %s)" % (self.S)

class Maze():
    # Class for full model of maze.
    def __init__(self, Size, Ball, Walls, Holes, Checkpoints):
        self.Size = Size
        self.Ball = Ball
        self.Walls = list(Walls)
        self.Holes = list(Holes)
        self.Checkpoints = list(Checkpoints) # Checkpoint order matters!

    def __repr__(self):
        # Printable.
        return "Maze(Size: %s, Ball: %s, Walls: %s, Holes: %s, Checkpoints: %s)" % (self.Size, self.Ball, self.Walls, self.Holes, self.Checkpoints)

    def update(self, TimeStep, Theta):
        self.Ball.update(TimeStep, Theta, self.Walls, self.Holes)
        return self.Ball.S

if __name__ == "__main__":
    import doctest
    doctest.testmod()
