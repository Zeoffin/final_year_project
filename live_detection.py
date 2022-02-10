"""
This is code for processing video stream from phone by using 'IP Webcam' app
"""

import requests
import numpy as np
import cv2 as cv

# Subject to change every time
url = "http://10.240.85.7:8080/shot.jpg"

# Initiate SIFT detector
sift = cv.SIFT_create()

img1 = cv.imread("Images/desktop.png", cv.IMREAD_GRAYSCALE)           # queryImage

# Setup for stream
cv.namedWindow("stream", cv.WINDOW_NORMAL)
cv.resizeWindow("stream", 900, 600)

# Find the keypoints for the desktop image
kp1, des1 = sift.detectAndCompute(img1, None)

while True:

    # TODO: What happens now, is that it is processing every frame. This should be limited. Threading? Seperate process?
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img2 = cv.imdecode(img_arr, -1)

    # find the keypoints and descriptors with SIFT
    kp2, des2 = sift.detectAndCompute(img2, None)

    # Descriptor is empty when there is nothing to detect (picture is completely dark/black)
    if des2 is not None:
        # BFMatcher with default params
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []

        # If the distance is less than %
        for m, n in matches:
            if m.distance < 0.6*n.distance:
                good.append([m])

        top_left, bot_right = 0, 0

        kp1_good = []     # Keypoints that we are interested in

        for i in good:
            for x in i:
                kp1_good.append(kp1[x.queryIdx].pt)     # Sorted by ascending X coordinate value

        # Display rectangle only if detecting features
        if len(kp1_good) > 0:
            kp1_good_y = sorted(kp1_good, key=lambda x_val: x_val[-1])

            # Get edges
            bot_right = (int(kp1_good[-1][0]), int(kp1_good_y[-1][1]))  # max(x) / max(y)
            top_left = (int(kp1_good[0][0]), int(kp1_good_y[0][1]))   # min(x) / min(y)

            print(f'Top left: {top_left} / Bot right: {bot_right}')

            # Draw the detected region
            cv.rectangle(img2, top_left, bot_right, (255, 0, 0), 2)  # Draws a rectangle

        cv.imshow("stream", img2)

    if cv.waitKey(1) == 27:    # ESC to exit
        break
