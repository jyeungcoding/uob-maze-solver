#!/usr/bin/env python3
'''
This file contains a class for the control calibration system. If all input positions
are within the calibration tolerane of the last position in the buffer, self.CalibrationDone
is outputted as True and the average of the input control signals over this time is outputted
as
'''

# Import modules.
import numpy as np

# Import settings.
from settings import CalibrationTolerance, CalibrationTime

class Calibrator():

    def __init__(self):
        # Initialise buffers and ouputs.
        self.PositionBuffer = []
        self.ThetaBuffer = []
        self.TimeBuffer = []
        self.ControlSignalCalibrated = np.array([0, 0])
        self.CalibrationDone = False

    def __repr__(self):
        # Makes the class printable.
        return "PID Controller(Kp: %s, Ki: %s, Kd: %s, Set Point: %s)" % (self.Kp, self.Ki, self.Kd, self.SetPoint)

    def update(self, Position, Theta, Time):
        # Add inputs to buffers.
        self.PositionBuffer.append(Position)
        self.ThetaBuffer.append(Theta)
        self.TimeBuffer.append(Time)
        # If buffer is filled over CalibrationTime, remove the last values and initialise CalibrationDone.
        if Time - self.TimeBuffer[0] > CalibrationTime:
            self.PositionBuffer.pop(0)
            self.ThetaBuffer.pop(0)
            self.TimeBuffer.pop(0)
            self.CalibrationDone = True
        # CalibrationDone doesn't remain true unless CalibrationTolerance is met.
        self.ReferencePosition = self.PositionBuffer[0]
        for Position in self.PositionBuffer:
            if (Position[0] - self.ReferencePosition[0]) ** 2 > CalibrationTolerance ** 2:
                self.CalibrationDone = False
            elif (Position[1] - self.ReferencePosition[1]) ** 2 > CalibrationTolerance ** 2:
                self.CalibrationDone = False
        # Calculate ControlSignalCalibrated if CalibrationDone is true. 
        if self.CalibrationDone == True:
            self.ControlSignalCalibrated = sum(self.ThetaBuffer) / len(self.ThetaBuffer)

        return self.CalibrationDone, self.ControlSignalCalibrated

if __name__ == "__main__":
    import doctest
    doctest.testmod()
