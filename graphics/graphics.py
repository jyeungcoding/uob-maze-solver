#!/usr/bin/env python3
'''
This file contains functions used to generate certain graphical objects in Pygame.
'''

# Import modules.
import pygame
import numpy as np

# Import classes and settings.
from graphics.objects import SpriteBall, SpriteWall, SpriteHole, SpriteCheckpoint, SpriteHeader, SpriteText, SpriteButton, SpriteVariableButton
from settings import White

def initialise_background(Size):
    # Generate background surface.
    Background = pygame.Surface((Size[0], Size[1]))
    Background.fill(White)
    Background.convert()
    return Background

def initialise_holes(Holes):
    # Generate holes.
    SpriteHoles = []
    for hole in Holes:
        SpriteHole_ = SpriteHole(
            hole.S, # [mm], numpy vector, size 2.
            hole.R # [mm], numpy vector, size 2.
        )
        SpriteHoles.append(SpriteHole_)
    return iter(SpriteHoles)

def initialise_walls(Walls):
    # Generate walls.
    SpriteWalls = []
    for wall in Walls:
        SpriteWall_ = SpriteWall(
            wall.S, # [mm], numpy vector, size 2.
            wall.Size # [mm], numpy vector, size 2.
        )
        SpriteWalls.append(SpriteWall_)
    return iter(SpriteWalls)

def initialise_checkpoints(Checkpoints):
    # Generate checkpoints.
    SpriteCheckPoints = []
    for checkpoint in Checkpoints:
        if Checkpoints.index(checkpoint) == 0: # First checkpoint is the set point.
            SpriteSetPoint_ = SpriteCheckpoint(
                checkpoint.S, # [mm], numpy vector, size 2.
                "SetPoint" # Checkpoint type.
            )
            SpriteCheckPoints.append(SpriteSetPoint_)
        elif Checkpoints.index(checkpoint) < len(Checkpoints) - 1:
            SpriteCheckpoint_ = SpriteCheckpoint(
                checkpoint.S, # [mm], numpy vector, size 2.
                "Checkpoint" # Checkpoint type.
            )
            SpriteCheckPoints.append(SpriteCheckpoint_)
        else: # Last checkpoint is coloured purple instead of blue.
            SpriteEndPoint_ = SpriteCheckpoint(
                checkpoint.S, # [mm], numpy vector, size 2.
                "EndPoint" # Checkpoint type.
            )
            SpriteCheckPoints.append(SpriteEndPoint_)
    return iter(SpriteCheckPoints)

def initialise_keys():
    # Generate ouput text keys.
    SpriteKeys = (
    SpriteText("Time Elapsed [s]: ", np.array([515, 65])),
    SpriteText("Position [mm]: ", np.array([515, 100])),
    SpriteText("P [°]: ", np.array([515, 135])),
    SpriteText("I [°]: ", np.array([515, 170])),
    SpriteText("D [°]: ", np.array([515, 205])),
    SpriteText("Saturation: ", np.array([515, 240])),
    SpriteText("Control Signal [°]: ", np.array([515, 275])),
    SpriteText("Theta [°]: ", np.array([515, 310]))
    )
    return SpriteKeys

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

def initialise_dirty_group(Maze):
    # Create dirty sprite group.
    ActiveSprites = pygame.sprite.LayeredDirty()
    # Generate holes, add to ActiveSprites.
    ActiveSprites.add(initialise_holes(Maze.Holes), layer = 0)
    # Generate walls, add to ActiveSprites.
    ActiveSprites.add(initialise_walls(Maze.Walls), layer = 1)
    # Generate checkpoints, add to ActiveSprites.
    ActiveSprites.add(initialise_checkpoints(Maze.Checkpoints), layer = 2)
    # Generate keys, add to ActiveSprites.
    ActiveSprites.add(initialise_keys(), layer = 3)
    return ActiveSprites

def initialise_buttons():
    # Initialise buttons.
    Buttons = pygame.sprite.LayeredDirty() # Create Dirty Sprite Group.
    Buttons.add(SpriteVariableButton(np.array([515, 350]), ("Start", "Stop")), layer = 0)
    Buttons.add(SpriteVariableButton(np.array([658, 350]), ("Maze 1", "Maze 2", "Maze 3")), layer = 0)
    Buttons.add(SpriteButton(np.array([515, 415]), "Reset"), layer = 0)
    Buttons.add(SpriteButton(np.array([658, 415]), "Quit"), layer = 0)
    return Buttons

def initialise_header():
    # Initialise header.
    SpriteHeader_ = SpriteHeader()
    return SpriteHeader_

def initialise_ball(Ball):
    SpriteBall_ = SpriteBall(
        Ball.S, # Initialise ball outside maze.
        Ball.R # [mm], numpy vector, size 2.
    )
    return SpriteBall_

def change_maze(Group, Maze):
    Group.remove_sprites_of_layer(0)
    Group.add(initialise_holes(Maze.Holes), layer = 0)
    Group.remove_sprites_of_layer(1)
    Group.add(initialise_walls(Maze.Walls), layer = 1)
    Group.remove_sprites_of_layer(2)
    Group.add(initialise_checkpoints(Maze.Checkpoints), layer = 2)
    return Group

if __name__ == "__main__":
    import doctest
    doctest.testmod()
