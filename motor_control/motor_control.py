#!/usr/bin/env python3

# Add "dtoverlay=pwm-2chan" to /boot/config.txt before you start.
# pin12 is now pwm0 and pin35 is now pwm1.

import os
from math import pi

#motor_limit = [7.2,17,26.8] # Duty cycle for Hitec at: 0 90 180
motor_limit = [8.3,16.1,22.7] # Duty cycle for Blue Bird at: 0 90 160

motor_steps = ((motor_limit[1] - motor_limit[0]) / (0.5 * pi)) # The factor of the on time
default_OnTime = 100000 * motor_limit[1]

def motor_reset(): # Start the PWM
    # For pin12
    os.system('sudo echo 0 > /sys/class/pwm/pwmchip0/export') # Exported  the hardware pwm channel
    os.system('sudo echo 12500000 > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm0/period') # Set up the period, which is 0.01s.
    os.system('sudo echo ' + str(int(default_OnTime)) + ' > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm0/duty_cycle') # Set up the on time, which makes the motor reset to 90 degree.
    os.system('sudo echo 1 > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm0/enable') # Enable the pwm output

    # For pin35
    os.system('sudo echo 1 > /sys/class/pwm/pwmchip0/export')
    os.system('sudo echo 10000000 > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm1/period')
    os.system('sudo echo ' + str(int(default_OnTime)) + ' > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm1/duty_cycle')
    os.system('sudo echo 1 > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm1/enable')

def motor_angle(Theta): # Enter the new angle
    # Theta (radians) should be a size 2 vector of floats. i.e. np.array([0.2 * pi, 0.2 * pi])
    OnTime = 100000 * (Theta * motor_steps + motor_limit[1]) # New on times

    # For pin12
    os.system('sudo echo ' + str(int(OnTime[0])) + ' > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm0/duty_cycle') # Set up the new on time for the new angle.
    # For pin35
    os.system('sudo echo ' + str(int(OnTime[1])) + ' > /sys/devices/platform/soc/fe20c000.pwm/pwm/pwmchip0/pwm1/duty_cycle')

if __name__ == "__main__":
    import doctest
    doctest.testmod()
