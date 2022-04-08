#!/usr/bin/env python3
'''
This file stores the Maze objects for Maze 1,2 and 3.
'''

# Import modules.
import numpy as np
from math import pi

# Import objects and settings.
from simulation.objects import CircleMaze, SandboxMaze
from objects import Maze, Ball, Wall, Hole, Checkpoint
from settings import FrameSize, MazeSize

# Calculate width of frame side.
FrameSide = (FrameSize - MazeSize) / 2

''' MAZE 1 START '''
Ball1 = Ball(np.array([FrameSide[0] + 123, FrameSide[1] + 8]))

Walls1 = [
Wall(np.array([154,0]), np.array([6,47])),
Wall(np.array([160,41]), np.array([15,6])),
Wall(np.array([37,15]), np.array([117,6])),
Wall(np.array([37,21]), np.array([6,9])),
Wall(np.array([18,47]), np.array([6,24])),
Wall(np.array([24,53]), np.array([93,6])),
Wall(np.array([111,59]), np.array([6,91])),
Wall(np.array([117,72]), np.array([53,6])),
Wall(np.array([54,150]), np.array([103,6])),
Wall(np.array([102,156]), np.array([6,25])),
Wall(np.array([48,144]), np.array([6,39])),
Wall(np.array([28,177]), np.array([26,6])),
Wall(np.array([0,141]), np.array([20,6])),
Wall(np.array([0,111]), np.array([91,6])),
Wall(np.array([34,96]), np.array([6,15])),
Wall(np.array([70,96]), np.array([6,15])),
Wall(np.array([74,181]), np.array([6,49])),
Wall(np.array([80,203]), np.array([109,6])),
Wall(np.array([136,186]), np.array([6,17])),
Wall(np.array([196, 21]), np.array([21, 6])),
Wall(np.array([211, 27]), np.array([6, 20])),
Wall(np.array([217, 41]), np.array([24, 6])),
Wall(np.array([222, 47]), np.array([6, 133])),
Wall(np.array([255, 56]), np.array([20, 6])),
Wall(np.array([250, 119]), np.array([25, 6])),
Wall(np.array([228, 154]), np.array([18, 6])),
Wall(np.array([182, 96]), np.array([40, 6])),
Wall(np.array([102, 102]), np.array([6, 106])),
Wall(np.array([188, 154]), np.array([34, 6])),
Wall(np.array([210, 196]), np.array([6, 34]))
]

Holes1 = [
Hole(np.array([33, 44])),
Hole(np.array([58, 102])),
Hole(np.array([34, 163])),
Hole(np.array([174, 191])),
Hole(np.array([150, 118])),
Hole(np.array([172, 60])),
Hole(np.array([239, 86])),
Hole(np.array([240, 170]))
]

for Wall in Walls1:
    Wall.S = Wall.S + FrameSide

for Hole in Holes1:
    Hole.S = Hole.S + FrameSide

Maze1 = Maze(Ball1, Walls1, Holes1, [])

Maze1Points = ((124, 10), (70, 10, (8, 2, np.array([None, None]))), (7, 107), (100, 68), (105, 110), (68, 148), (48, 130, (6, 2, np.array([None, None]))), (5, 180, (8, 0, np.array([-pi/4, pi/4]))), (64, 225), (68, 168), (90, 170), (95, 197), (120, 197), (118, 165), (171, 148), (135, 145), (125, 93), (218, 71), (163, 7), (270, 7), (270, 49), (233, 67), (269, 113), (233, 148), (268, 180), (231, 210), (192, 168, (8, 0, np.array([-pi/4, None]))), (92, 222))

for Point in Maze1Points:
    if len(Point) == 2:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates)
        Maze1.Checkpoints.append(Checkpoint_)
    elif len(Point) == 3:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates, True, Point[2][0], Point[2][1], Point[2][2]) # Order: radius, time, hard control signal.
        Maze1.Checkpoints.append(Checkpoint_)
''' MAZE 1 END '''

''' MAZE 2 START '''
Ball2 = Ball(np.array([FrameSide[0] + 158, FrameSide[1] + 12]))

Maze2 = Maze(Ball2, [], [], [])

Maze2Points = ((160, 11), (52, 12), (43, 77), (76, 127), (5, 119), (4, 190), (39, 190), (87, 178), (75, 141), (120, 141), (119, 190), (130, 190), (142, 189), (143, 170), (142, 149), (140, 136), (128, 117), (113, 103), (90, 102), (107, 26), (123, 27), (121, 54), (196, 59), (184, 24), (266, 23), (267, 67), (205, 87), (166, 136), (205, 125), (220, 221), (101, 220))

for Point in Maze2Points:
    if len(Point) == 2:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates)
        Maze2.Checkpoints.append(Checkpoint_)
    elif len(Point) == 3:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates, True, Point[2][0], Point[2][1], Point[2][2]) # Order: radius, time, hard control signal.
        Maze2.Checkpoints.append(Checkpoint_)
''' MAZE 2 END '''

"""
''' MAZE 3 START '''
Ball3 = Ball(np.array([FrameSide[0] + 142, FrameSide[1] + 17]))

Maze3 = Maze(Ball3, [], [], [])

Maze3Points = ((142, 17), (128, 17), (112, 17), (99, 17), (85, 17), (83, 18), (83, 22), (82, 26), (81, 29), (78, 30), (74, 31), (69, 31), (66, 31), (64, 30), (62, 29), (61, 25), (60, 21), (59, 17), (54, 16), (49, 15), (40, 15), (38, 18), (38, 23), (38, 28), (38, 32), (37, 33), (35, 34), (32, 35), (26, 35), (20, 35), (17, 35), (15, 37), (15, 48), (15, 59), (15, 63), (21, 63), (27, 63), (32, 63), (36, 63), (38, 66), (39, 70), (39, 77), (38, 81), (28, 82), (21, 82), (15, 83), (15, 90), (15, 96), (15, 101), (18, 103), (22, 102), (27, 102), (33, 102), (38, 103), (40, 103), (40, 108), (40, 117), (40, 124), (39, 133), (39, 136), (31, 137), (24, 137), (18, 138), (16, 139), (15, 141), (16, 146), (16, 153), (16, 158), (17, 161), (21, 165), (25, 168), (31, 171), (33, 176), (35, 179), (35, 183), (31, 186), (29, 191), (27, 193), (26, 197), (24, 200), (24, 205), (24, 210), (25, 213), (28, 215), (36, 215), (45, 215), (54, 215), (58, 212), (60, 209), (64, 206), (68, 202), (71, 200), (75, 196), (80, 191), (84, 188), (87, 184), (87, 180), (87, 174), (85, 172), (83, 170), (80, 168), (76, 167), (72, 167), (69, 166), (67, 161), (67, 157), (67, 153), (72, 149), (75, 145), (78, 143), (83, 143), (91, 143), (97, 142), (103, 142), (106, 141), (107, 137), (106, 131), (107, 127), (107, 122), (107, 113), (107, 110), (106, 105), (104, 103), (99, 103), (93, 103), (89, 103), (86, 102), (82, 100), (79, 98), (75, 95), (71, 93), (68, 90), (64, 88), (62, 86), (62, 81), (62, 75), (62, 71), (62, 67), (63, 62), (67, 62), (74, 62), (79, 62), (86, 62), (92, 62), (98, 62), (104, 62), (107, 61), (106, 56), (106, 52), (107, 48), (107, 45), (107, 41), (113, 40), (120, 40), (125, 40), (128, 42), (129, 50), (127, 58), (128, 63), (128, 68), (130, 70), (132, 70), (136, 70), (141, 70), (145, 70), (148, 71), (149, 75), (149, 80), (149, 85), (149, 89), (149, 94), (149, 97), (149, 100), (148, 101), (146, 103), (145, 103), (142, 104), (139, 105), (134, 105), (130, 105), (128, 107), (127, 110), (127, 114), (127, 117), (127, 121), (128, 125), (128, 128), (129, 133), (129, 136), (131, 138), (135, 138), (140, 138), (146, 138), (149, 138), (148, 142), (149, 146), (150, 150), (150, 153), (147, 155), (142, 156), (137, 156), (132, 157), (130, 157), (127, 160), (127, 165), (127, 168), (127, 171), (127, 174), (124, 175), (119, 176), (113, 176), (107, 177), (106, 185), (107, 192), (106, 202), (107, 212), (117, 212), (126, 212), (137, 212), (147, 212), (150, 211), (150, 208), (150, 204), (150, 198), (150, 193), (150, 188), (150, 185), (155, 183), (158, 180), (161, 179), (164, 177), (166, 175), (168, 173), (172, 172), (178, 172), (182, 172), (186, 172), (189, 172), (193, 173), (192, 181), (193, 190), (193, 199), (194, 207), (193, 213), (202, 212), (212, 213), (215, 212), (215, 205), (215, 196), (215, 186), (215, 184), (220, 183), (226, 183), (231, 182), (237, 182), (241, 182), (243, 179), (248, 175), (252, 171), (255, 168), (255, 162), (252, 158), (249, 154), (246, 151), (242, 149), (239, 145), (236, 141), (235, 135), (235, 130), (235, 123), (234, 117), (230, 115), (223, 115), (218, 116), (215, 116), (214, 118), (213, 126), (213, 133), (214, 137), (214, 142), (212, 144), (203, 145), (195, 144), (192, 139), (192, 134), (192, 131), (184, 131), (178, 131), (173, 132), (170, 130), (171, 122), (170, 117), (170, 112), (170, 108), (174, 106), (177, 103), (180, 99), (184, 96), (188, 93), (191, 90), (194, 87), (195, 86), (199, 86), (205, 85), (210, 85), (212, 84), (213, 81), (213, 78), (213, 76), (213, 72), (213, 70), (210, 69), (206, 68), (202, 68), (197, 68), (193, 68), (192, 62), (192, 59), (192, 48), (193, 34), (193, 32), (204, 31), (210, 30), (213, 30), (217, 30), (222, 30), (227, 31), (230, 31), (233, 31), (235, 34), (237, 37), (238, 41), (238, 46), (238, 50), (238, 56), (237, 60), (238, 65), (238, 69), (238, 71), (240, 72), (244, 72), (249, 72), (253, 73), (257, 73), (256, 79), (256, 82), (255, 95), (256, 105), (256, 117))

for Point in Maze3Points:
    if len(Point) == 2:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates)
        Maze3.Checkpoints.append(Checkpoint_)
    elif len(Point) == 3:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates, True, Point[2][0], Point[2][1], Point[2][2]) # Order: radius, time, hard control signal.
        Maze3.Checkpoints.append(Checkpoint_)
''' MAZE 3 END '''
"""

''' MAZE 3 START '''
Ball3 = Ball(np.array([FrameSide[0] + 142, FrameSide[1] + 17]))

Maze3 = Maze(Ball3, [], [], [])

# Please replace these with the actual mazes.
Maze3Points = ((135, 9), (4, 3), (4, 108), (30, 107), (108, 63), (109, 146), (58, 147), (50, 119), (3, 184), (4, 224), (68, 224), (98, 160), (132, 198), (178, 124), (122, 146), (123, 81), (219, 51), (163, 4), (271, 4), (271, 50), (232, 67), (271, 113), (233, 149), (271, 224), (222, 222), (192, 164), (194, 222), (84, 220))

for Point in Maze3Points:
    if len(Point) == 2:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates)
        Maze3.Checkpoints.append(Checkpoint_)
    elif len(Point) == 3:
        Coordinates = np.array([Point[0], Point[1]]) + FrameSide
        Checkpoint_ = Checkpoint(Coordinates, True, Point[2][0], Point[2][1], Point[2][2]) # Order: radius, time, hard control signal.
        Maze3.Checkpoints.append(Checkpoint_)
''' MAZE 3 END '''

if __name__ == "__main__":
    if type(Maze1) != Maze:
        raise TypeError("Maze1 should be of class Maze. See 'objects.py'.")
    elif type(Maze2) != Maze:
        raise TypeError("Maze2 should be of class Maze. See 'objects.py'.")
    elif type(Maze3) != Maze:
        raise TypeError("Maze3 should be of class Maze. See 'objects.py'.")
