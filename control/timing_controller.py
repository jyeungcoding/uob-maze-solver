#!/usr/bin/env python3
'''
This file contains a class for the timing controller system, which generates control
signals for the control and graphic functions in the main code based on the timing
settings in settings.py.
'''

# Import modules.
from settings import ControlFrequency, GraphicsFrequency

class TimingController():

    def __init__(self, Time):
        self.ControlPeriod = 1 / ControlFrequency # Calculate period from frequency.
        self.GraphicsPeriod = 1 / GraphicsFrequency

        self.ControlOn = True # Control signal for control loop.
        self.ControlTimeStep = 0 # Save next time step of control loop.
        self.LastControl = Time # Save last time ControlOn was True.
        self.GraphicsOn = True # Control signal for graphics loop.
        self.LastGraphics = Time # Save last time GraphicsOn was True.

    def __repr__(self):
        # Makes the class printable.
        return "Timing Controller(ControlOn: %s, LastControl: %s, GraphicsOn: %s, LastGraphics: %s)" % (self.ControlOn, round(self.LastControl, 2), self.GraphicsOn, round(self.LastGraphics, 2))

    def update(self, Time):
        if Time - self.LastControl > self.ControlPeriod:
            self.ControlOn = True
            self.ControlTimeStep = Time - self.LastControl
            self.LastControl = Time
        else:
            self.ControlOn = False

        if Time - self.LastGraphics > self.GraphicsPeriod:
            self.GraphicsOn = True
            self.LastGraphics = Time
        else:
            self.GraphicsOn = False

        return self.ControlOn, self.ControlTimeStep, self.GraphicsOn

if __name__ == "__main__":
    import doctest
    doctest.testmod()
