#!/usr/bin/env python3
'''
This file contains a class for the a simple timer that measures the time
between updates.
'''

class PerformanceTimer():

    def __init__(self, Time):
        self.LastTime = Time

    def __repr__(self):
        # Makes the class printable.
        return "Timer(Last Time: %s)" % (round(self.LastControl, 2))

    def update(self, Time):
        TimeStep = Time - self.LastTime
        self.LastTime = Time
        return TimeStep

if __name__ == "__main__":
    import doctest
    doctest.testmod()
