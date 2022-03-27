#!/usr/bin/env python3
'''
This file contains functions used to generate certain graphical objects in Pygame.
'''

# Import modules.
import pygame
import numpy as np

# Import classes and settings.
from graphics.objects import SpriteBall, SpriteWall, SpriteHole, SpriteCheckpoint, SpriteHeader, SpriteText, SpriteButton, SpriteVariableButton

def initialise_keys():
    # Generate ouput text keys.
    Sprites = (
    SpriteText("Time Elapsed [s]: ", np.array([515, 65])),
    SpriteText("Position [mm]: ", np.array([515, 100])),
    SpriteText("P [°]: ", np.array([515, 135])),
    SpriteText("I [°]: ", np.array([515, 170])),
    SpriteText("D [°]: ", np.array([515, 205])),
    SpriteText("Saturation: ", np.array([515, 240])),
    SpriteText("Control Signal [°]: ", np.array([515, 275])),
    SpriteText("Theta [°]: ", np.array([515, 310]))
    )
    return Sprites

def initialise_background(Holes, Walls):
    BackgroundSprites = pygame.sprite.LayeredUpdates() # Create LayeredUpdates Sprite Group.
    for hole in Holes:
        # Generate holes.
        SpriteHole_ = SpriteHole(
            hole.S, # [mm], numpy vector, size 2.
            hole.R # [mm], numpy vector, size 2.
        )
        BackgroundSprites.add(SpriteHole_, layer = 0)
    for wall in Walls:
        # Generate walls.
        SpriteWall_ = SpriteWall(
            wall.S, # [mm], numpy vector, size 2.
            wall.Size # [mm], numpy vector, size 2.
        )
        BackgroundSprites.add(SpriteWall_, layer = 1)
    #Generate display keys.
    BackgroundSprites.add(initialise_keys(), layer = 2)
    return BackgroundSprites

def initialise_checkpoints(Checkpoints):
    # Generate checkpoints.
    ActiveSprites = pygame.sprite.LayeredDirty() # Create Dirty Sprite Group.
    for checkpoint in Checkpoints:
        if Checkpoints.index(checkpoint) == 0: # First checkpoint is the set point.
            SpriteSetPoint_ = SpriteCheckpoint(
                checkpoint.S, # [mm], numpy vector, size 2.
                "SetPoint" # Checkpoint type.
            )
            ActiveSprites.add(SpriteSetPoint_, layer = 0)
        elif Checkpoints.index(checkpoint) < len(Checkpoints) - 1:
            SpriteCheckpoint_ = SpriteCheckpoint(
                checkpoint.S, # [mm], numpy vector, size 2.
                "Checkpoint" # Checkpoint type.
            )
            ActiveSprites.add(SpriteCheckpoint_, layer = 0)
        else: # Last checkpoint is coloured purple instead of blue.
            SpriteEndPoint_ = SpriteCheckpoint(
                checkpoint.S, # [mm], numpy vector, size 2.
                "EndPoint" # Checkpoint type.
            )
            ActiveSprites.add(SpriteEndPoint_, layer = 0)
    return ActiveSprites

def initialise_ball(Ball):
    SpriteBall_ = SpriteBall(
        Ball.S, # [mm], numpy vector, size 2.
        Ball.R # [mm], numpy vector, size 2.
    )
    return SpriteBall_

def initialise_header():
    # Initialise header. 
    SpriteHeader_ = SpriteHeader()
    return SpriteHeader_

def initialise_values():
    # Initialise ouput text values.
    Sprites = (
    SpriteText("0.0s", np.array([664, 65])),
    SpriteText("( 0.0 , 0.0 )", np.array([644, 100])),
    SpriteText("( 0.0 , 0.0 )", np.array([563, 135])),
    SpriteText("( 0.0 , 0.0 )", np.array([560, 170])),
    SpriteText("( 0.0 , 0.0 )", np.array([567, 205])),
    SpriteText("( False , False )", np.array([610, 240])),
    SpriteText("( 0.0 , 0.0 )", np.array([672, 275])),
    SpriteText("( 0.0 , 0.0 )", np.array([599, 310]))
    )
    return Sprites

def initialise_buttons():
    # Initialise buttons.
    Buttons = pygame.sprite.LayeredDirty() # Create Dirty Sprite Group.
    Buttons.add(SpriteVariableButton(np.array([515, 350]), ("Start", "Stop")), layer = 0)
    Buttons.add(SpriteVariableButton(np.array([658, 350]), ("Maze 1", "Maze 2", "Maze 3")), layer = 0)
    Buttons.add(SpriteButton(np.array([515, 415]), "Reset"), layer = 0)
    Buttons.add(SpriteButton(np.array([658, 415]), "Quit"), layer = 0)
    return Buttons

if __name__ == "__main__":
    import doctest
    doctest.testmod()
