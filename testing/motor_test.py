#!/usr/bin/env python3
'''
This file contains functions used to test and calibrate the motor control function.
'''

# Import modules.
import numpy as np
from math import pi
from time import sleep

# Import functions.
from motor_control.motor_control import motor_angle, motor_reset

def test1():
    motor_reset()
    motor_angle(np.array([-pi, -pi]))
    sleep(1)
    motor_angle(np.array([0, 0]))
    sleep(1)
    motor_angle(np.array([pi, pi]))

def test2():
    motor_reset()
    motor_angle(np.array([-pi, -pi]))
    sleep(1)
    motor_angle(np.array([-0.5 * pi, -0.5 * pi]))
    sleep(1)
    motor_angle(np.array([0, 0]))
    sleep(1)
    motor_angle(np.array([0.5 * pi, 0.5 * pi]))
    sleep(1)
    motor_angle(np.array([pi, pi]))

def test3():
    motor_reset()
    motor_angle(np.array([0, 0]))
    sleep(10)
    motor_angle(np.array([0.02 * pi, 0.02 * pi]))
    sleep(0.5)
    motor_angle(np.array([0, 0]))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
