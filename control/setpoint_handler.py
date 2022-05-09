#!/usr/bin/env python3
'''
This file contains the set point handler which controls two output signals:
self.MazeCompleted is set to 1 when the last checkpoint has been reached, and
self.NewSetPoint is set to True when the current set point has been reached.
self.NewSetPoint indicates that a new set point should be given to the PID
controller. 
'''

# Import modules.
import numpy as np

class SetPointHandler():

    def __init__(self, BallPosition, CurrentTime, Checkpoints, CheckpointRadius, SetPointTime):
        # Save checkpoints and settings.
        self.Checkpoints = Checkpoints
        self.DefaultSetPointTime = SetPointTime
        self.DefaultCheckpointRadius = CheckpointRadius

        self.SetPoint = self.Checkpoints[0].S # Set set point as first checkpoint.
        if self.Checkpoints[0].Special == True: # Override default checkpoint settings if checkpoint is special.
            self.SetPointTime = self.Checkpoints[0].Time
            self.CheckpointRadius = self.Checkpoints[0].Radius
        else: # Otherwise, use default settings.
            self.SetPointTime = self.DefaultSetPointTime
            self.CheckpointRadius = self.DefaultCheckpointRadius

        # Initialise some values.
        self.LastTime = CurrentTime
        self.SetPointReached = False
        self.MazeCompleted = 0
        self.NewSetPoint = False

    def __repr__(self):
        # Makes the class printable.
        return "SetPointHandler(Current set point: %s)" % (self.SetPoint)

    def new_setpoint(self):
        # Function for progressing to the next set point.
        if len(self.Checkpoints) > 1:
            self.Checkpoints.pop(0) # Delete current checkpoint.
            self.SetPoint = self.Checkpoints[0].S # Set set point as first checkpoint.
            if self.Checkpoints[0].Special == True: # Override default checkpoint settings if checkpoint is special.
                self.SetPointTime = self.Checkpoints[0].Time
                self.CheckpointRadius = self.Checkpoints[0].Radius
            else: # Otherwise, use default settings.
                self.SetPointTime = self.DefaultSetPointTime
                self.CheckpointRadius = self.DefaultCheckpointRadius
        else:
            self.MazeCompleted = 1 # If the last checkpoint has been reached, the program has been completed.

    def update(self, BallPosition, CurrentTime):
        if ((BallPosition[0] - self.SetPoint[0]) ** 2 + (BallPosition[1] - self.SetPoint[1]) ** 2) ** 0.5 < self.CheckpointRadius:
            # If the ball is inside the set point radius.
            if self.SetPointReached == False: # Record the time when the ball enters the set point's raidus.
                self.LastTime = CurrentTime
            self.NewSetPoint = False
            self.SetPointReached = True # Record that the ball is inside the set point radius.
        else: # Otherwise, reset values.
            self.NewSetPoint = False
            self.SetPointReached = False

        if self.SetPointReached == True and CurrentTime - self.LastTime >= self.SetPointTime:
            # If the ball is inside the set point radius and the minimum amount of time has passed.
            self.new_setpoint() # Progress to the next set point.
            self.NewSetPoint = True # Output the NewSetPoint signal as True.
            self.SetPointReached = False # Reset value.

        return self.MazeCompleted, self.NewSetPoint, self.Checkpoints

if __name__ == "__main__":
    import doctest
    doctest.testmod()
