#!/usr/bin/env python3
'''
This file contains the set point handler.
'''

# Import modules.
import numpy as np

class SetPointHandler():

    def __init__(self, SetPoint, CheckpointRadius, SetPointTime):

        self.SetPoint = SetPoint
        self.SetPointTime = SetPointTime
        self.CheckpointRadius = CheckpointRadius

        self.SetPointReached = False

    def __repr__(self):
        # Makes the class printable.
        return "SetPointHandler(SetPoint: %s)" % (self.SetPoint)

    def new_setpoint(self, SetPoint):
        self.SetPointReached = False
        self.SetPoint = SetPoint

    def update(self, Position, CurrentTime):
        SetPointCompleted = False
        if self.SetPointReached == False:
            if ((Position[0] - self.SetPoint[0]) ** 2 + (Position[1] - self.SetPoint[1]) ** 2) ** 0.5 < self.CheckpointRadius:
                self.SetPointReached = True
                self.StartTime = CurrentTime
        else:
            if ((Position[0] - self.SetPoint[0]) ** 2 + (Position[1] - self.SetPoint[1]) ** 2) ** 0.5 < self.CheckpointRadius:
                if CurrentTime - self.StartTime > self.SetPointTime:
                    SetPointCompleted = True
            else:
                self.SetPointReached = False

        return SetPointCompleted

if __name__ == "__main__":
    import doctest
    doctest.testmod()
