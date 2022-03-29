#!/usr/bin/env python3

# Add "dtoverlay=pwm-2chan" to /boot/config.txt before you start.
# pin12 is now pwm0 and pin35 is now pwm1.
# Duty cycles: 0.01125 for -60, 0.019 for 0, 0.02625 for 60

import numpy as np
from math import pi
from rpi_hardware_pwm import HardwarePWM

class MotorController():

    def __init__(self):
        self.DutyCycles = (4.5, 7.5, 10.5)
        self.MaxAngle = pi / 2
        self.DutyCycleChange = {
        "-1" : self.DutyCycles[1] - self.DutyCycles[0],
        "0" : 0,
        "1" : self.DutyCycles[2] - self.DutyCycles[1]
        }
        self.pwm0 = HardwarePWM(pwm_channel=0, hz=50)
        self.pwm1 = HardwarePWM(pwm_channel=1, hz=50)

    def start(self):
        self.pwm0.start(self.DutyCycles[1])
        self.pwm1.start(self.DutyCycles[1])

    def change_angle(self, Theta):

        ThetaSigns = np.sign(Theta)

        Multiplier = np.array([self.DutyCycleChange[str(int(ThetaSigns[0]))], self.DutyCycleChange[str(int(ThetaSigns[1]))]])

        AngleProportion = Theta / np.array([self.MaxAngle, self.MaxAngle])

        DutyCycle = AngleProportion * Multiplier + self.DutyCycles[1]

        self.pwm0.change_duty_cycle(DutyCycle[0])
        self.pwm1.change_duty_cycle(DutyCycle[1])

    def stop(self):
        self.pwm0.stop()
        self.pwm1.stop()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
