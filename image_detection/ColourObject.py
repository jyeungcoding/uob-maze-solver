import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    Gauss_frame = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv_frame = cv2.cvtColor(Gauss_frame, cv2.COLOR_BGR2HSV)

    # Red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    red = cv2.bitwise_and(frame, frame, mask=red_mask)
    """
    # Blue color
    low_blue = np.array([94, 80, 2])
    high_blue = np.array([126, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)
    
    # Green color
    low_green = np.array([25, 52, 72])
    high_green = np.array([102, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, mask=green_mask)
    """
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        np.array([])

    # ((x, y), radius) = cv2.minEnclosingCircle(c)
    centers = np.zeros((len(contours), 2), dtype=np.int32)
    for i, c in enumerate(contours):
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        else:
            center = (0, 0)

        centers[i] = center
    cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)
    print(centers)

    # print(contours)

    cv2.imshow("Frame", frame)
    cv2.imshow("Red", red)
    #cv2.imshow("Blue", blue)
    #cv2.imshow("Green", green)
    # cv2.imshow("Result", result)

    key = cv2.waitKey(5)
    if key == 27:
        break
