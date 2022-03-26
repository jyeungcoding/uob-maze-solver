#!/usr/bin/env python3
'''
This file contains object classes derived from the pygame Sprite class needed for graphically displaying the maze.
'''

# Import modules.
import pygame
import numpy as np

# Import values.
from settings import DisplayScale, GUIScale, HeaderShift, White, Black, Grey, DimGrey, CheckpointColours

class SpriteBall(pygame.sprite.DirtySprite):
    # Sprite class for the metal ball.
    def __init__(self, Position, Radius):
        # Position should be provided in a numpy vector, size 2. Units in mm. Radius should be provided in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Size for GUI.
        self.LastPosition = Position
        Position = Position * GUIScale + HeaderShift
        Radius = Radius * GUIScale
        # Sets sprite image as a circle.
        self.image = pygame.Surface((2 * Radius + 1, 2 * Radius + 1), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.circle(self.image, Black, (round(Radius), round(Radius)), round(Radius)) # pygame.draw requires int inputs on Linux but not on Mac.
        self.image.convert() # Convert surface to same pixel format as display for faster blitting.
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] # Ball position in pixels, based on center of ball.
        self.rect.centery = Position[1] # Ball position in pixels, based on center of ball.

    def update(self, Position):
        # Only update if position has changed.
        if np.array_equal(Position, self.LastPosition) == False:
            Position = Position * GUIScale + HeaderShift # Size for GUI.
            self.rect.centerx = Position[0] # Ball position in pixels, based on center of ball.
            self.rect.centery = Position[1] # Ball position in pixels, based on center of ball.
            self.dirty = 1 # Set for redraw.
            self.LastPosition = Position

class SpriteHole(pygame.sprite.Sprite):
    # Sprite class for holes.
    def __init__(self, Position, Radius):
        # Position should be provided in a numpy vector, size 2. Units in mm. Radius should be provided in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")

        super().__init__()
        # Size for GUI.
        Position = Position * GUIScale + HeaderShift
        Radius = Radius * GUIScale
        # Sets sprite image as a circle.
        self.image = pygame.Surface((2 * Radius + 1, 2 * Radius + 1), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.circle(self.image, DimGrey, (round(Radius), round(Radius)), round(Radius)) # pygame.draw requires int inputs on Linux but not on Mac.
        self.image.convert() # Convert surface to same pixel format as display for faster blitting.
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] # Hole position in pixels, based on center of hole.
        self.rect.centery = Position[1] # Hole position in pixels, based on center of hole.

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
        # Size for GUI.
        Position = Position * GUIScale + HeaderShift
        Size = Size * GUIScale
        # Sets sprite image as a surface.
        self.image = pygame.Surface((Size[0], Size[1])) # Wall dimensions in pixels.
        self.image.fill(Grey)
        self.image.convert() # Convert surface to same pixel format as display for faster blitting.
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = Position[0] # Wall position in pixels.
        self.rect.y = Position[1] # Wall position in pixels.

class SpriteCheckpoint(pygame.sprite.DirtySprite):
    # Sprite class for checkpoints.
    def __init__(self, Position, Type):
        # Position should be provided in a numpy vector, size 2. Units in mm.
        if type(Position) != np.ndarray:
            raise TypeError("Position should be given in a size 2 numpy array.")
        elif Position.shape != (2,):
            raise ValueError("Position should be given in a size 2 numpy array.")
        if Type != "SetPoint" and Type != "Checkpoint" and Type != "EndPoint":
            raise ValueError("Type should be 'SetPoint', 'Checkpoint' or 'EndPoint'.")

        super().__init__()
        # Size for GUI.
        self.Position = Position * GUIScale + HeaderShift
        # Different colour for each checkpoint type.
        self.Type = Type # Save type.
        # Sets sprite image as a cross.
        self.image = pygame.Surface((5 * GUIScale + 1, 5 * GUIScale + 1), pygame.SRCALPHA) # Convert to pixels.
        pygame.draw.line(self.image, CheckpointColours[self.Type], (0, 0), (round(4 * GUIScale), round(4 * GUIScale)), round(GUIScale))
        pygame.draw.line(self.image, CheckpointColours[self.Type], (0, round(4 * GUIScale)), (round(4 * GUIScale), 0), round(GUIScale))
        self.image.convert() # Convert surface to same pixel format as display for faster blitting.
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = self.Position[0] # Checkpoint position in pixels, based on center of checkpoint.
        self.rect.centery = self.Position[1] # Checkpoint position in pixels, based on center of checkpoint.

    def update(self, Type):
        # Only update if position has changed.
        if Type != self.Type:
            self.Type = Type  # Save type.
            # Sets sprite image as a cross.
            self.image = pygame.Surface((5 * GUIScale + 1, 5 * GUIScale + 1), pygame.SRCALPHA) # Convert to pixels.
            pygame.draw.line(self.image, CheckpointColours[self.Type], (0, 0), (round(4 * GUIScale), round(4 * GUIScale)), round(GUIScale))
            pygame.draw.line(self.image, CheckpointColours[self.Type], (0, round(4 * GUIScale)), (round(4 * GUIScale), 0), round(GUIScale))
            self.image.convert() # Convert surface to same pixel format as display for faster blitting.
            # Creates sprite rect object for positioning.
            self.rect = self.image.get_rect()
            self.rect.centerx = self.Position[0] # Checkpoint position in pixels, based on center of checkpoint.
            self.rect.centery = self.Position[1] # Checkpoint position in pixels, based on center of checkpoint.
            self.dirty = 1 # Set for redraw.

class SpriteText(pygame.sprite.DirtySprite):
    # Sprite class for GUI variable text.
    def __init__(self, String, Font, Position):
        super().__init__()
        self.String = String # Save value.
        self.Font = Font # Save value.
        self.Position = Position * DisplayScale # Save value.
        # Create surface with text.
        self.image = self.Font.render(String, True, Black, White)
        # Create sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = self.Position[0] # Text position in pixels.
        self.rect.y = self.Position[1] # Text position in pixels.

    def update(self, String):
        # Only update if value has changed.
        if self.String != String:
            # Create surface with text.
            self.image = self.Font.render(String, True, Black, White)
            # Create sprite rect object for positioning.
            self.rect = self.image.get_rect()
            self.rect.x = self.Position[0] # Text position in pixels.
            self.rect.y = self.Position[1] # Text position in pixels.
            # Mark for redraw.
            self.dirty = 1 # Set for redraw.
            self.String = String # Save value.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
