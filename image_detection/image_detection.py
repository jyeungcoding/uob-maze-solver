#!/usr/bin/env python3
'''
This file contains a class for the image detection system, including all memory elements
and functions needed to fetch the position of the checkpoitns and the ball.
'''

# Import modules.
import cv2
import numpy as np

# Import classes.
from simulation.objects import SandboxMaze, SimpleMaze, CircleMaze

class Image_Detector():

    def __init__(self, StartTime):

        self.LastPosition = np.array([0, 0])
        self.StartTime = StartTime
        self.LastTime = StartTime

    def __repr__(self):
        # Makes the class printable.
        return "Image Detector(Last Ball Position: %s, Time Taken: %s)" % (self.LastPosition, round((self.LastTime - self.StartTime), 2))

    def initialise_maze(self):
        '''
        This function is run once at the beginning of the program. It captures all elements in the
        maze (ball and checkpoints) and outputs a single Maze object as defined in
        'objects.py'. Please check 'objects.py' for the required specifications. Please remember
        that the y axis starts at the top left corner and increases as you go down the maze,
        opposite to a traditional coordinate system. Furthermore, the side frames of the maze are
        included in the coordiate system so the "true" area where maze objects can exists should
        be from (28.75, 28.25) to (303.25, 257.75). Do check this based on the frame and maze
        sizes in the settings file though.
        '''

        '''
        Include redundancy for ball not found.
        '''

        '''
        This function is currently not used.
        '''

        return SandboxMaze

    def update_ball(self, Cap, CurrentTime):
        '''
        This function is run during every processing loop to update the position of the ball in
        our maze objects. The output should be in the format of a tuple: Active, Position.
        Active should be a boolean value and should be set to True as long as the ball is still
        on the maze, and False when the ball has fallen through a hole. The Position of the Ball
        should be provided as np.array([x, y]). See objects.py for more information.
        '''

        _, frame1 = Cap.read()
        frame = frame1[6:480, 62: 606]
        Gauss_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv_frame = cv2.cvtColor(Gauss_frame, cv2.COLOR_BGR2HSV)
        """
        # Red color
        low_red = np.array([161, 155, 84])
        high_red = np.array([179, 255, 255])
        red_mask = cv2.inRange(hsv_frame, low_red, high_red)
        red = cv2.bitwise_and(frame, frame, mask=red_mask)
        """
        # Blue color
        low_blue = np.array([94, 80, 2])
        high_blue = np.array([126, 255, 255])
        blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
        blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
        """
        # Green color
        low_green = np.array([25, 52, 72])
        high_green = np.array([102, 255, 255])
        green_mask = cv2.inRange(hsv_frame, low_green, high_green)
        green = cv2.bitwise_and(frame, frame, mask=green_mask)
        """
        contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) == 0:
            #np.array([])
            if CurrentTime - self.LastTime > 5:
                Active = False
                Position = np.array([0, 0])
            else:
                Active = True
                Position = self.LastPosition

        # ((x, y), radius) = cv2.minEnclosingCircle(c)
        #centers = np.zeros((len(contours), 2), dtype=np.int32)
        for i, c in enumerate(contours):
            area = cv2.contourArea(c)
            M = cv2.moments(c)  # Moment calculation required to get centre
            if M["m00"] != 0 and area > 100:
                self.LastTime = CurrentTime
                Active = True
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))   # Equation to get centre of contour
                Position = np.array(((center[0] / 1.176), (center[1] / 1.012658)), dtype=np.int32)
                self.LastPosition = Position
            else:
                if CurrentTime - self.LastTime > 5:
                    Active = False
                    Position = np.array([0, 0])
                else:
                    Active = True
                    Position = self.LastPosition
            #centers[i] = center

        cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)

        #cv2.imshow("Frame", frame)
        #cv2.imshow("Red", red)
        #cv2.imshow("Blue", blue)
        #cv2.imshow("Green", green)
        # cv2.imshow("Result", result)

        return Active, Position

if __name__ == "__main__":
    import doctest
    doctest.testmod()
