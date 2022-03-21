import cv2
import numpy as np

# Load Image  
image = cv2.imread('image2.png') 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(gray, 30, 200)
  
# Finding Contours
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  
# Draw all contours
'''
for x in range(len(contours)):
    cv2.drawContours(image, contours, x, (0,0,255), 3)
    cv2.waitKey(0)
    print(x)
    cv2.imshow('Original', image)
                     
'''
# Choosing only one contour
cv2.drawContours(image, contours, 290, (0, 0, 255), 3)

# Display
cv2.imshow('Contours', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
