#!/usr/bin/env python3
'''
This file contains the function needed to simulate manual tilting of the
maze with the arrow keys to ThetaStep in each direction. Utilises pyagme.
'''

# Import modules.
import pygame

# Import classes and settings.
from settings import ThetaStep

def tilt_maze(event, Theta):
    # Manual maze tilt using arrow keys, returns theta of maze in radians.
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            Theta[0] -= ThetaStep # Tilt angle defined in settings.
        elif event.key == pygame.K_RIGHT:
            Theta[0] += ThetaStep
        elif event.key == pygame.K_UP:
            Theta[1] -= ThetaStep
        elif event.key == pygame.K_DOWN:
            Theta[1] += ThetaStep
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
            Theta[0] += ThetaStep
        elif event.key == pygame.K_RIGHT:
            Theta[0] -= ThetaStep
        elif event.key == pygame.K_UP:
            Theta[1] += ThetaStep
        elif event.key == pygame.K_DOWN:
            Theta[1] -= ThetaStep
    return Theta # Size 2 numpy array of floats.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
