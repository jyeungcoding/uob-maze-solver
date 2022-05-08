#!/usr/bin/env python3

# Import modules.
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

LightImage = mpimg.imread('1.jpg')
LightImageHSV = matplotlib.colors.rgb_to_hsv(LightImage)
DarkImage = mpimg.imread('2.jpg')
DarkImageHSV = matplotlib.colors.rgb_to_hsv(DarkImage)

plt.subplot(221)
plt.imshow(LightImage)
plt.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
plt.xlabel("(a) Light image: RGB")

plt.subplot(222)
plt.imshow(LightImageHSV)
plt.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
plt.xlabel("(b) Light image: HSV")

plt.subplot(223)
plt.imshow(DarkImage)
plt.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
plt.xlabel("(c) Dark image: RGB")

plt.subplot(224)
plt.imshow(DarkImageHSV)
plt.tick_params(left = False, labelleft = False, bottom = False, labelbottom = False)
plt.xlabel("(d) Dark image: HSV")

plt.show()
