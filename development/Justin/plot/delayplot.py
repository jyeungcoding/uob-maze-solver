#!/usr/bin/env python3

# Import modules.
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Plot a box diagram of control loop time.

ReadFile = open("log.txt", "rt")
Text = ReadFile.read()
ReadFile.close()

Times = np.array([])

for Row in Text.split("\n"):
    Row = Row.split(" ")
    Text = Row[-1]
    Number = float(''.join([Digit for Digit in Text if Digit.isdigit() or Digit == "."])) # [ms]
    Times = np.append(Times, Number)

Mean = np.mean(Times)

plt.figure(figsize=(16, 5))
plt.subplot(221)
#plt.rcParams.update({'font.size': 16}) # Change font size.
Dict = plt.boxplot(Times, sym = "", vert = False, widths = 0.05)
plt.tick_params(left = False, labelleft = False)
plt.xlim([60, 142])
plt.ylim([0.95, 1.05])
plt.xlabel("Control loop time [ms]")
plt.text(112, 0.97, "".join(("Mean: ", str(round(Mean, 1)), "ms")))
plt.show()
