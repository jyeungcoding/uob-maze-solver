#!/usr/bin/env python3
'''
This file stores the Maze objects for Maze 1,2 and 3.
'''

# Import modules.
import numpy as np

from objects import Maze, Ball, Checkpoint

# Delete this line when you're done:
from simulation.objects import SandboxMaze, SimpleMaze, CircleMaze

file = open("maze1points.txt", 'r')
text = file.read()
file.close()

textpoints = text.split("\n")

textpoints = [textpoint.split(",") for textpoint in textpoints]

points = [np.array([28.75 + int(point[0]), 28.25 + int(point[1])]) for point in textpoints]

Ball1 = Ball(np.array([28.75 + 123, 28.25 + 10]))

Maze1 = Maze(Ball1, [], [], [])

for point in points:
    Checkpoint_ = Checkpoint(point)
    Maze1.Checkpoints.append(Checkpoint_)

# Please replace these with the actual mazes.
Maze2 = SimpleMaze
Maze3 = CircleMaze

if __name__ == "__main__":
    if type(Maze1) != Maze:
        raise TypeError("Maze1 should be of class Maze. See 'objects.py'.")
    elif type(Maze2) != Maze:
        raise TypeError("Maze2 should be of class Maze. See 'objects.py'.")
    elif type(Maze3) != Maze:
        raise TypeError("Maze3 should be of class Maze. See 'objects.py'.")
