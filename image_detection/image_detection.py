#!/usr/bin/env python3
'''
This file contains the main functions needed to capture all elements in the maze and represent
it as a single Maze object as defined in 'objects.py'.
'''

from objects import Ball, Wall, Hole, Checkpoint, Maze

def initialise_maze():
    '''
    This function is run once at the beginning of the program. It captures all elements in the
    maze (ball, walls, holes and checkpoints) and outputs a single Maze object as defined in
    'objects.py'. Please check 'objects.py' for the required specifications. Please remember
    that the y axis starts at the top left corner and increases as you go down the maze,
    opposite to a traditional coordinate system. Furthermore, the side frames of the maze are
    included in the coordiate system so the "true" area where maze objects can exists should
    be from (28.75, 28.25) to (303.25, 257.75). Do check this based on the frame and maze
    sizes in the settings file though.
    '''

    return Maze

def update_ball():
    '''
    This function is run during every processing loop to update the position of the ball in
    our maze objects. The output should be in the format of a tuple: Active, Position.
    Active should be a boolean value and should be set to True as long as the ball is still
    on the maze, and False when the ball has fallen through a hole. The Position of the Ball
    should be provided as np.array([x, y]). See objects.py for more information.
    '''

    from picamera.array import PiRGBArray
    from picamera import PiCamera
    import time
    import cv2
    import numpy as np

    Active = 1

    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.rotation = 180
    rawCapture = PiRGBArray(camera, size=(640, 480))
    firstFrame = None

    # allow the camera to adjust to lighting/white balance
    time.sleep(2)

    # initiate video or frame capture sequence
    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw array representation of the image
        frame = f.array

        # convert images to grayscale &  blur the result
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # initialize firstFrame which will be used as a reference
        if firstFrame is None:
            firstFrame = gray
            rawCapture.truncate(0)
            continue

        # obtain difference between frames
        frameDelta = cv2.absdiff(gray, firstFrame)

        # coonvert the difference into binary & dilate the result to fill in small holes
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # show the result
        cv2.imshow("Delta + Thresh", thresh)

        # find contours or continuous white blobs in the image
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_SIMPLE)  # Try CV_RETR_EXTERNAL to remove largest contour if statement

        # find the index of the largest contour
        if len(contours) > 0:
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt = contours[max_index]

            # draw a bounding box/rectangle around the largest contour
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # area = cv2.contourArea(cnt)

            # Finding Centre of contour by using moments and centroid calculation
            M = cv2.moments(thresh)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            Position = np.array([cX, cY])

            # print area to the terminal
            # print(area)

            # add text to the frame
            cv2.putText(frame, "Largest Contour", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # show the frame
        cv2.imshow("Video", frame)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the 'q' key is pressed then break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    return Active, Position

if __name__ == "__main__":
    import doctest
    doctest.testmod()