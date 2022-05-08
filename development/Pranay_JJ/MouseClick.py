import cv2
import numpy as np

def mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)


cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse)

while True:
    _, frame = cap.read()
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

