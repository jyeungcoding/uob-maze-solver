#!/usr/bin/env python3
'''
This file stores the Maze objects for Maze 1,2 and 3.
'''

# Import modules.
import numpy as np

# Delete this line when you're done:
from simulation.objects import SandboxMaze, SimpleMaze, CircleMaze

# Please replace these with the actual mazes.
Maze1 = SandboxMaze
Maze2 = SimpleMaze
Maze3 = CircleMaze

if __name__ == "__main__":
    if type(Maze1) != Maze:
        raise TypeError("Maze1 should be of class Maze. See 'objects.py'.")
    elif type(Maze2) != Maze:
        raise TypeError("Maze2 should be of class Maze. See 'objects.py'.")
    elif type(Maze3) != Maze:
        raise TypeError("Maze3 should be of class Maze. See 'objects.py'.")
