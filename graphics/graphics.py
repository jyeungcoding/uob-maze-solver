#!/usr/bin/env python3
'''
This file contains functions used to generate certain graphical objects in Pygame.
'''

# Import modules.
import pygame

# Import classes and settings.
from graphics.objects import SpriteWall, SpriteHole, SpriteCheckpoint

def initialise_walls(Walls):
    # Generate walls.
    WallList = pygame.sprite.Group()
    for wall in Walls:
        SpriteWall1 = SpriteWall(
            wall.S, # [mm], numpy vector, size 2.
            wall.Size # [mm], numpy vector, size 2.
        )
        WallList.add(SpriteWall1)
    return WallList

def initialise_holes(Holes):
    # Generate holes.
    HoleList = pygame.sprite.Group()
    for hole in Holes:
        SpriteHole1 = SpriteHole(
            hole.S, # [mm], numpy vector, size 2.
            hole.R # [mm], numpy vector, size 2.
        )
        HoleList.add(SpriteHole1)
    return HoleList

def initialise_checkpoints(Checkpoints):
    # Generate checkpoints.
    CheckpointList = pygame.sprite.Group()
    for checkpoint in Checkpoints:

        Checkpoint1 = SpriteCheckpoint(
            checkpoint.S, # [mm], numpy vector, size 2.
        )
        CheckpointList.add(Checkpoint1)
    return CheckpointList

if __name__ == "__main__":
    import doctest
    doctest.testmod()
