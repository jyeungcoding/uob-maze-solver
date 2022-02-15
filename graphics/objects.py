#!/usr/bin/env python3
'''
This file contains object classes derived from the pygame Sprite class needed for graphically displaying the maze.
'''

# Import modules.
import pygame
import numpy as np

# Import values.
from settings import PixelScale, Black, Grey, DimGrey, Red, Blue, Purple

class SpriteBall(pygame.sprite.Sprite):
    # Sprite class for the metal ball.
    def __init__(self, Position, Radius):
        # Position should be provided in a numpy vector, size 2. Units in mm. Radius should be provided in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Sets sprite image as a circle.
        self.shape = pygame.Surface((2 * Radius * PixelScale, 2 * Radius * PixelScale), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.circle(self.shape, Black, (Radius * PixelScale, Radius * PixelScale), Radius * PixelScale)
        self.image = self.shape
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] * PixelScale # Ball position in pixels, based on center of ball.
        self.rect.centery = Position[1] * PixelScale # Ball position in pixels, based on center of ball.

class SpriteWall(pygame.sprite.Sprite):
    # Sprite class for walls.
    def __init__(self, Position, Size):
        # Position and size should be provided in numpy vectors, size 2. Units in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")
        if type(Size) != np.ndarray:
            raise TypeError("Size should be given in a size 2 numpy array.")
        elif Size.shape != (2,):
            raise ValueError("Size should be given in a size 2 numpy array.")

        super().__init__()
        # Sets sprite image as a surface.
        self.image = pygame.Surface((Size[0] * PixelScale, Size[1] * PixelScale)) # Wall dimensions in pixels.
        self.image.fill(Grey)
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = Position[0] * PixelScale # Wall position in pixels.
        self.rect.y = Position[1] * PixelScale # Wall position in pixels.

class SpriteHole(pygame.sprite.Sprite):
    # Sprite class for holes.
    def __init__(self, Position, Radius):
        # Position should be provided in a numpy vector, size 2. Units in mm. Radius should be provided in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Sets sprite image as a circle.
        self.shape = pygame.Surface((2 * Radius * PixelScale, 2 * Radius * PixelScale), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.circle(self.shape, DimGrey, (Radius * PixelScale, Radius * PixelScale), Radius * PixelScale)
        self.image = self.shape
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] * PixelScale # Hole position in pixels, based on center of hole.
        self.rect.centery = Position[1] * PixelScale # Hole position in pixels, based on center of hole.

class SpriteCheckpoint(pygame.sprite.Sprite):
    # Sprite class for checkpoints.
    def __init__(self, Position):
        # Position should be provided in a numpy vector, size 2. Units in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Sets sprite image as a cross.
        self.shape = pygame.Surface((8 * PixelScale, 8 * PixelScale), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.line(self.shape, Blue, (0, 0), (8, 8), 3)
        pygame.draw.line(self.shape, Blue, (0, 8), (8, 0), 3)
        self.image = self.shape
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] * PixelScale # Checkpoint position in pixels, based on center of checkpoint.
        self.rect.centery = Position[1] * PixelScale # Checkpoint position in pixels, based on center of checkpoint.

class SpriteSetPoint(pygame.sprite.Sprite):
    # Sprite class for the current set point.
    def __init__(self, Position):
        # Position should be provided in a numpy vector, size 2. Units in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Sets sprite image as a cross.
        self.shape = pygame.Surface((8 * PixelScale, 8 * PixelScale), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.line(self.shape, Red, (0, 0), (8, 8), 3)
        pygame.draw.line(self.shape, Red, (0, 8), (8, 0), 3)
        self.image = self.shape
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] * PixelScale # Set point position in pixels, based on center of set point.
        self.rect.centery = Position[1] * PixelScale # Set point position in pixels, based on center of set point.

class SpriteEndPoint(pygame.sprite.Sprite):
    # Sprite class for the last checkpoint.
    def __init__(self, Position):
        # Position should be provided in a numpy vector, size 2. Units in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Sets sprite image as a cross.
        self.shape = pygame.Surface((8 * PixelScale, 8 * PixelScale), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.line(self.shape, Purple, (0, 0), (8, 8), 3)
        pygame.draw.line(self.shape, Purple, (0, 8), (8, 0), 3)
        self.image = self.shape
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] * PixelScale # Set point position in pixels, based on center of set point.
        self.rect.centery = Position[1] * PixelScale # Set point position in pixels, based on center of set point.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
