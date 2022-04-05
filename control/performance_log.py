#!/usr/bin/env python3
'''
This file contains a class for the a performance logger that records the timesteps
and control signals of each loop. A maximum of 30 entries are saved at a time.
'''

class PerformanceLog():

    def __init__(self, Time):
        # Initilise LastTime and Log.
        self.LastTime = Time
        self.Log = []

    def __repr__(self):
        # Makes the class printable.
        return "PerformanceLog:\n%" % ("\n".join(self.Log))

    def update(self, ControlOn, GraphicsOn, Time):
        # TimeStep calculation.
        TimeStep = Time - self.LastTime
        self.LastTime = Time
        # Save entry to log.
        LogEntry = "ControlOn: {}, GraphicsOn: {}, TimeStep: {}ms".format(ControlOn, GraphicsOn, TimeStep * 1000)
        self.Log.append(LogEntry)
        if len(self.Log) > 30: # If log has over 30 entries, pop the first entry.
            self.Log.pop(0)
        return LogEntry

    def export(self, Filename):
        # Export the log as a text file.
        LogFile = open(Filename, "wt")
        LogFile.write("\n".join(self.Log))
        LogFile.close()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
