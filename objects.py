#!/usr/bin/env python3

# Import modules.
import pygame
import numpy as np
from math import sin

# Import values.
from settings import PixelScale, Black, Grey

# Remember to check units!

class Ball(pygame.sprite.Sprite):
    #Class for the metal ball
    def __init__(self, Position, Velocity, Acceleration, Radius, Mass, Drag):
        # Position, velocity and acceleration should be provided in a numpy vector, size 2.
        super().__init__()
        # Sets sprite image as a circle.
        self.shape = pygame.Surface((2 * Radius * PixelScale, 2 * Radius * PixelScale), pygame.SRCALPHA) # Convert radius to pixels. 
        pygame.draw.circle(self.shape, Black, (Radius * PixelScale, Radius * PixelScale), Radius * PixelScale)
        self.image = self.shape
        # Creates sprite mask for collision detection.
        self.mask = pygame.mask.from_surface(self.image)
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] * PixelScale # Ball position in pixels based on center of ball.
        self.rect.centery = Position[1] * PixelScale # Ball position in pixels based on center of ball.

        self.S = Position # Standard units (see settings).
        self.v = Velocity # Standard units (see settings).
        self.a = Acceleration # Standard units (see settings).
        self.r = Radius # Standard units (see settings).
        self.mass = Mass # Standard units (see settings).
        self.drag = Drag # Standard units (see settings).

    def __repr__(self):
        # Printable.
        return "Ball(Position: %s, Velocity: %s, Acceleration: %s, Radius: %s, Mass: %s, Drag: %s)" % (self.S, self.v, self.a, self.r, self.mass, self.drag)

    def next_a(self, Theta):
        # NewA[mm/s^2] = gsin(theta)*1000
        NewA = 9.81 * np.sin(Theta) * 1000
        # Artificial drag on ball: approximates air resistance and friction.
        NewA -= self.drag * self.v
        #print(NewA)
        return NewA

    def next_v(self, TimeStepS, NewA):
        NewV = self.v + (self.a + NewA) * TimeStepS / 2
        #print(NewV)
        return NewV

    def next_S(self, TimeStepS, NewV):
        NewS = self.S + (self.v + NewV) * TimeStepS / 2
        #print(NewS)
        return NewS

    def wall_collision(self, WallList):
        # Corners do not exist
        WallHitList = pygame.sprite.spritecollide(self, WallList, True, pygame.sprite.collide_mask)
        for wall in WallHitList:
            CollisionPoint = pygame.sprite.collide_mask(self, wall) # Approximately the collision point.
        return WallHitList

    def update(self, TimeStepMs, Theta, WallList):
        TimeStepS = TimeStepMs / 1000
        # Process motion.
        self.a = self.next_a(Theta)
        self.v = self.next_v(TimeStepS, self.a)
        self.S = self.next_S(TimeStepS, self.v)

        # Process collisions.
        self.wall_collision(WallList)

        # Update the ball's rect location.
        self.rect.x = self.S[0]
        self.rect.y = self.S[1]

class Wall(pygame.sprite.Sprite):
    # Class for walls.
    def __init__(self, Position, Size):
        # Position and size should be provided in numpy vectors, size 2.
        super().__init__()
        # Sets sprite image as a surface.
        self.image = pygame.Surface((Size[0] * PixelScale, Size[1] * PixelScale)) # Wall dimensions in pixels.
        self.image.fill(Grey)
        # Creates sprite mask for collision detection.
        self.mask = pygame.mask.from_surface(self.image)
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = Position[0] * PixelScale # Wall position in pixels.
        self.rect.y = Position[1] * PixelScale # Wall position in pixels.

        self.S = Position # Standard units (see settings).
        self.D = Size # Standard units (see settings).

    def __repr__(self):
        # Printable.
        return "Wall(Position: %s, Size: %s)" % (self.S, self.D)

if __name__ == "__main__":
    import doctest
    doctest.testmod()