#!/usr/bin/env python3
'''
'main.py' runs each of the testing, simulation or main control functions depending on
the input command line argument. See the header in each function's file for a more
detailed description of what they do. If no argument is provided the default main
control function is run.
'''

# Import modules.
from sys import argv

# Import functions.
from full_system import full_system
from testing.image_detection_test import image_detection_test
from simulation.manual_sim import manual_sim
from simulation.pid_sim import pid_sim
from testing.motor_test import test1, test2, test3
from testing.model_tuning import model_tuning

def main():
    if len(argv) == 2 and argv[1].isdigit():
        if int(argv[1]) == 0:
            image_detection_test()
        elif int(argv[1]) == 1:
            manual_sim() # Simulation of manual tilt.
        elif int(argv[1]) == 2:
            pid_sim() # PID control simulation. 
        elif int(argv[1]) == 3:
            test1() # Motor test.
        elif int(argv[1]) == 4:
            test2() # Motor test.
        elif int(argv[1]) == 5:
            test3() # Motor test.
        elif int(argv[1]) == 6:
            model_tuning() # Simulated model tuning.
    else:
        full_system()

if __name__ == "__main__":
    main()
