#!/usr/bin/env python3
'''
This file contains object classes derived from the pygame Sprite class needed for graphically displaying the maze.
'''

# Import modules.
import pygame
import numpy as np
from itertools import cycle

# Import values.
from settings import DisplayScale, GUIScale, HeaderShift, White, Black, Grey, DimGrey, LightGreen, LightRed, CheckpointColours, HeaderFont, TextFont, ButtonFont

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

class SpriteHole(pygame.sprite.DirtySprite):
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
        self.image = pygame.Surface((2 * Radius + 1, 2 * Radius + 1)) # Convert to pixels.
        self.image.fill(White) # Set white background.
        pygame.draw.circle(self.image, DimGrey, (round(Radius), round(Radius)), round(Radius)) # pygame.draw requires int inputs on Linux but not on Mac.
        self.image.convert() # Convert surface to same pixel format as display for faster blitting.
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.centerx = Position[0] # Hole position in pixels, based on center of hole.
        self.rect.centery = Position[1] # Hole position in pixels, based on center of hole.

class SpriteWall(pygame.sprite.DirtySprite):
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
        self.image = pygame.Surface((5 * GUIScale + 1, 5 * GUIScale + 1)) # Convert to pixels.
        self.image.fill(White) # Set white background.
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
            self.image.fill(White) # Set white background.
            pygame.draw.line(self.image, CheckpointColours[self.Type], (0, 0), (round(4 * GUIScale), round(4 * GUIScale)), round(GUIScale))
            pygame.draw.line(self.image, CheckpointColours[self.Type], (0, round(4 * GUIScale)), (round(4 * GUIScale), 0), round(GUIScale))
            self.image.convert() # Convert surface to same pixel format as display for faster blitting.
            # Creates sprite rect object for positioning.
            self.rect.centerx = self.Position[0] # Checkpoint position in pixels, based on center of checkpoint.
            self.rect.centery = self.Position[1] # Checkpoint position in pixels, based on center of checkpoint.
            self.dirty = 1 # Set for redraw.

class SpriteHeader(pygame.sprite.DirtySprite):
    # Sprite class for GUI header.
    def init_text_surface(self, Text, Colour):
        # Create text surface.
        TextSurface = HeaderFont.render(Text, True, Black, Colour) # Generate text surface.
        if TextSurface.get_size()[0] > 800 or TextSurface.get_size()[1] > 51:
            raise ValueError("Text is larger than button.")
        XPosition = round((800 - TextSurface.get_size()[0]) / 2) # Generate x position for centered text.
        YPosition = round((51 - TextSurface.get_size()[1]) / 2) # Generate y position for centered text.
        return TextSurface, XPosition, YPosition

    def init_surface(self, Text, Colour):
        # Create header surface.
        Surface = pygame.Surface((800, 51)) # Header dimensions in pixels.
        Surface.fill(Colour) # Background colour.
        TextSurface, XPosition, YPosition = self.init_text_surface(Text, Colour) # Create text surface.
        Surface.blit(TextSurface, (XPosition, YPosition)) # Blit text onto header surface.
        Surface = pygame.transform.scale(Surface, (round(800 * DisplayScale), round(51 * DisplayScale))) # Scale by DisplayScale.
        Surface.convert() # Convert surface to same pixel format as display for faster blitting.
        return Surface

    def __init__(self):
        super().__init__()
        # Defined statuses.
        Statuses_Green = ("Ready", "Calibrating", "Running", "Completed")
        Statuses_Red = ("Paused", "Ball Lost / Not Found")

        # Generate surfaces for each status.
        self.Surfaces = {}
        for Status in Statuses_Green:
            self.Surfaces[Status] = self.init_surface(Status, LightGreen)
        for Status in Statuses_Red:
            self.Surfaces[Status] = self.init_surface(Status, LightRed)

        # Save current status.
        self.CurrentStatus = "Ready"
        # Set correct surface as image.
        self.image = self.Surfaces["Ready"]
        # Create sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = 0 # Text position in pixels.
        self.rect.y = 0 # Text position in pixels.

    def update(self, Status):
        # Only update if status has changed.
        if Status != self.CurrentStatus:
            # Update surface.
            self.image = self.Surfaces[Status]
            # Create sprite rect object for positioning.
            self.rect = self.image.get_rect()
            self.rect.x = 0 # Text position in pixels.
            self.rect.y = 0 # Text position in pixels.

            self.dirty = 1 # Set for redraw.
            self.CurrentStatus = Status

class SpriteText(pygame.sprite.DirtySprite):
    # Sprite class for GUI variable text.
    def __init__(self, String, Position):
        super().__init__()
        self.String = String # Save value.
        self.Position = Position * DisplayScale # Save value.
        # Create surface with text.
        self.image = TextFont.render(String, True, Black, White)
        # Create sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = self.Position[0] # Text position in pixels.
        self.rect.y = self.Position[1] # Text position in pixels.

    def update(self, String):
        # Only update if value has changed.
        if self.String != String:
            # Create surface with text.
            self.image = TextFont.render(String, True, Black, White)
            # Create sprite rect object for positioning.
            self.rect = self.image.get_rect()
            self.rect.x = self.Position[0] # Text position in pixels.
            self.rect.y = self.Position[1] # Text position in pixels.
            # Mark for redraw.
            self.dirty = 1 # Set for redraw.
            self.String = String # Save value.

class SpriteButton(pygame.sprite.DirtySprite):
    # Sprite class for GUI buttons. State should be a string.
    def init_text_surface(self, Text):
        # Create text surface.
        TextSurface = ButtonFont.render(Text, True, Black, Grey) # Generate text surface.
        if TextSurface.get_size()[0] > 121 or TextSurface.get_size()[1] > 46:
            raise ValueError("Text is larger than button.")
        XPosition = round((121 - TextSurface.get_size()[0]) / 2) # Generate x position for centered text.
        YPosition = round((46 - TextSurface.get_size()[1]) / 2) # Generate y position for centered text.
        return TextSurface, XPosition, YPosition

    def init_up_surface(self, TextSurface, XPosition, YPosition):
        # Create button up surface.
        UpSurface = pygame.Surface((125, 50)) # Button dimensions in pixels.
        UpSurface.fill(Black) # For black border.
        InnerUpSurface = pygame.Surface((121, 46)) # Inner button area.
        InnerUpSurface.fill(Grey) # Grey background.
        InnerUpSurface.blit(TextSurface, (XPosition, YPosition)) # Blit text onto inner area.
        UpSurface.blit(InnerUpSurface, (1, 1)) # Blit inner area onto button.
        UpSurface = pygame.transform.scale(UpSurface, (round(125 * DisplayScale), round(50 * DisplayScale))) # Scale by DisplayScale.
        UpSurface.convert() # Convert surface to same pixel format as display for faster blitting.
        return UpSurface

    def init_down_surface(self, TextSurface, XPosition, YPosition):
        # Create button down surface.
        DownSurface = pygame.Surface((125, 50)) # Button dimensions in pixels.
        DownSurface.fill(Black) # For black border.
        InnerDownSurface = pygame.Surface((121, 46)) # Inner button area.
        InnerDownSurface.fill(Grey) # Grey background.
        InnerDownSurface.blit(TextSurface, (XPosition, YPosition)) # Blit text onto inner area.
        DownSurface.blit(InnerDownSurface, (3, 3)) # Blit inner area onto button.
        DownSurface = pygame.transform.scale(DownSurface, (round(125 * DisplayScale), round(50 * DisplayScale))) # Scale by DisplayScale.
        DownSurface.convert() # Convert surface to same pixel format as display for faster blitting.
        return DownSurface

    def __init__(self, Position, State):
        super().__init__()
        # Size for GUI.
        self.Position = Position * DisplayScale
        # Clicking.
        self.Clicked = False
        self.ClickTime = 0 # For button animation.
        self.CurrentState = State

        # Generate up and down surfaces.
        TextSurface, XPosition, YPosition = self.init_text_surface(State)
        self.Surfaces = (
        self.init_up_surface(TextSurface, XPosition, YPosition),
        self.init_down_surface(TextSurface, XPosition, YPosition)
        )

        self.image = self.Surfaces[0] # Begin with up surface.

        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = self.Position[0] # Wall position in pixels.
        self.rect.y = self.Position[1] # Wall position in pixels.

    def click(self, Time):
        # Button is clicked.
        self.Clicked = True
        self.ClickTime = Time # Record click time.
        # Change to down surface.
        self.image = self.Surfaces[1]
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = self.Position[0] # Wall position in pixels.
        self.rect.y = self.Position[1] # Wall position in pixels.
        self.dirty = 1 # Set for redraw.

    def update(self, Time):
        # Update button animation.
        if self.Clicked == True and Time > self.ClickTime + 0.4:
            self.Clicked = False
            # Change to up surface.
            self.image = self.Surfaces[0]
            # Creates sprite rect object for positioning.
            self.rect = self.image.get_rect()
            self.rect.x = self.Position[0] # Wall position in pixels.
            self.rect.y = self.Position[1] # Wall position in pixels.
            self.dirty = 1 # Set for redraw.

class SpriteVariableButton(SpriteButton):
    # Sprite class for variable GUI buttons. States entered in a tuple.
    def __init__(self, Position, States):
        super().__init__(Position, States[0])

        self.StateIterator = cycle(States) # Create infinite iterator of States.
        self.CurrentState = next(self.StateIterator)

        # Generate up and down surfaces for each state.
        self.Surfaces = {}
        for State in States:
            TextSurface, XPosition, YPosition = self.init_text_surface(State)
            self.Surfaces[State] = (
            self.init_up_surface(TextSurface, XPosition, YPosition),
            self.init_down_surface(TextSurface, XPosition, YPosition)
            )

    def click(self, Time):
        # Button is clicked.
        self.Clicked = True
        self.ClickTime = Time # Record click time.
        self.CurrentState = next(self.StateIterator) # Next state.
        # Change to down surface.
        self.image = self.Surfaces[self.CurrentState][1]
        # Creates sprite rect object for positioning.
        self.rect = self.image.get_rect()
        self.rect.x = self.Position[0] # Wall position in pixels.
        self.rect.y = self.Position[1] # Wall position in pixels.
        self.dirty = 1 # Set for redraw.

    def update(self, Time):
        # Update button animation.
        if self.Clicked == True and Time > self.ClickTime + 0.4:
            self.Clicked = False
            # Change to up surface of next state.
            self.image = self.Surfaces[self.CurrentState][0]
            # Creates sprite rect object for positioning.
            self.rect = self.image.get_rect()
            self.rect.x = self.Position[0] # Wall position in pixels.
            self.rect.y = self.Position[1] # Wall position in pixels.
            self.dirty = 1 # Set for redraw.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
