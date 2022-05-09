#!/usr/bin/env python3
'''
This file contains a class for the control calibration system. Ball position is continuously
saved to a buffer: self.CalibrationDone is set to True when all values in the buffer fulfil
the calibration conditions. The calibrated value is taken as the mean of the values in the
buffer.
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
        return "Calibrator(CalibrationDone: %s, ControlSignalCalibrated: %s)" % (self.CalibrationDone, self.ControlSignalCalibrated)

    def update(self, Position, Theta, Time):
        # Add inputs to buffers.
        self.PositionBuffer.append(Position)
        self.ThetaBuffer.append(Theta)
        self.TimeBuffer.append(Time)
        # If buffer is filled over CalibrationTime, remove the last values and initialise CalibrationDone as True.
        if Time - self.TimeBuffer[0] > CalibrationTime:
            self.PositionBuffer.pop(0)
            self.ThetaBuffer.pop(0)
            self.TimeBuffer.pop(0)
            self.CalibrationDone = True
        # CalibrationDone doesn't remain true unless CalibrationTolerance is met.
        for Position in self.PositionBuffer:
            if (Position[0] - self.PositionBuffer[0][0]) ** 2 > CalibrationTolerance ** 2:
                self.CalibrationDone = False
            elif (Position[1] - self.PositionBuffer[0][1]) ** 2 > CalibrationTolerance ** 2:
                self.CalibrationDone = False
        # Calculate ControlSignalCalibrated if CalibrationDone is True.
        if self.CalibrationDone == True:
            self.ControlSignalCalibrated = sum(self.ThetaBuffer) / len(self.ThetaBuffer)

        return self.CalibrationDone, self.ControlSignalCalibrated

if __name__ == "__main__":
    import doctest
    doctest.testmod()
