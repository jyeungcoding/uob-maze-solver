#!/usr/bin/env python3
'''
This file contains the set point handler.
'''

# Import modules.
import numpy as np

class SetPointHandler():

    def __init__(self, BallPosition, CurrentTime, Checkpoints, CheckpointRadius, SetPointTime):

        # Save checkpoints and settings.
        self.Checkpoints = Checkpoints
        self.DefaultSetPointTime = SetPointTime
        self.DefaultCheckpointRadius = CheckpointRadius

        self.SetPoint = self.Checkpoints[0].S
        if self.Checkpoints[0].Special == True:
            self.SetPointTime = self.Checkpoints[0].Time
            self.CheckpointRadius = self.Checkpoints[0].Radius
        else:
            self.SetPointTime = self.DefaultSetPointTime
            self.CheckpointRadius = self.DefaultCheckpointRadius

        # Initialise values.
        self.LastTime = CurrentTime
        self.SetPointReached = False
        self.MazeCompleted = 0
        self.NewSetPoint = False

    def __repr__(self):
        # Makes the class printable.
        return "SetPointHandler(SetPoint: %s)" % (self.SetPoint)

    def new_setpoint(self):
        if len(self.Checkpoints) > 1:
            self.Checkpoints.pop(0) # Delete current checkpoint.
            self.SetPoint = self.Checkpoints[0].S
            if self.Checkpoints[0].Special == True:
                self.SetPointTime = self.Checkpoints[0].Time
                self.CheckpointRadius = self.Checkpoints[0].Radius
            else:
                self.SetPointTime = self.DefaultSetPointTime
                self.CheckpointRadius = self.DefaultCheckpointRadius
        else:
            self.MazeCompleted = 1 # If the last checkpoint has been reached, the program has been completed.

    def update(self, BallPosition, CurrentTime):
        if ((BallPosition[0] - self.SetPoint[0]) ** 2 + (BallPosition[1] - self.SetPoint[1]) ** 2) ** 0.5 < self.CheckpointRadius:
            if self.SetPointReached == False:
                self.StartTime = CurrentTime
            self.NewSetPoint = False
            self.SetPointReached = True
        else:
            self.NewSetPoint = False
            self.SetPointReached = False

        if self.SetPointReached == True and CurrentTime - self.LastTime >= self.SetPointTime:
            self.new_setpoint()
            self.NewSetPoint = True
            self.SetPointReached = False

        return self.MazeCompleted, self.NewSetPoint, self.Checkpoints

if __name__ == "__main__":
    import doctest
    doctest.testmod()
