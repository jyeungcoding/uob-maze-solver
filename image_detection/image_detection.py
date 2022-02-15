#!/usr/bin/env python3
'''
This file contains the main functions needed to capture all elements in the maze and represent
it as a single Maze object as defined in 'objects.py'.
'''

from objects import Ball, Wall, Hole, Checkpoint, Maze

def initialise_maze():
    '''
    This function is run once at the beginning of the program. It captures all elements in the
    maze (ball, walls, holes and checkpoints) and outputs a single Maze object as defined in
    'objects.py'. Please check 'objects.py' for the required specifications. Please remember
    that the y axis starts at the top left corner and increases as you go down the maze,
    opposite to a traditional coordinate system. Furthermore, the side frames of the maze are
    included in the coordiate system so the "true" area where maze objects can exists should
    be from (28.75, 28.25) to (303.25, 257.75). Do check this based on the frame and maze
    sizes in the settings file though. 
    '''

    return Maze

def update_ball():
    '''
    This function is run during every processing loop to update the position of the ball in
    our maze objects. The output should be in the format of a list: [Active, Position].
    Active should be a boolean value and should be set to True as long as the ball is still
    on the maze, and False when the ball has fallen through a hole. The Position of the Ball
    should be provided as np.array([x, y]). See objects.py for more information.
    '''

    return Output

if __name__ == "__main__":
    import doctest
    doctest.testmod()
