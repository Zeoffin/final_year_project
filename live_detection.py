"""
This is code for processing video stream from phone by using 'IP Webcam' app
"""
from PIL import ImageGrab
from ppadb.client import Client as AdbClient

import time
import requests
import numpy as np
import threading
import cv2 as cv
import subprocess
import adblib_test

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
BEST_IMAGE_PERCENTAGE = 0.5

# Get the live feed from phone by using its IP address and app called 'IP Webcam'
url = "http://10.240.85.7:8080/video"
live_feed = cv.VideoCapture(url)

# Initiate SIFT detector
sift = cv.SIFT_create()

# Desktop image - to be replaced with live display capture
img1 = cv.imread("Images/desktop.png", cv.IMREAD_GRAYSCALE)

# Setup for stream
cv.namedWindow("stream", cv.WINDOW_NORMAL)
cv.resizeWindow("stream", WINDOW_WIDTH, WINDOW_HEIGHT)

# List for thread For threading management
image_processing_threads = []

# Parameters for drawing the matched region
top_left = None
bot_right = None
color = (255, 0, 0)
thickness = 2

# TODO: REMOVE WHEN DETECTING SCREEN
# Find the keypoints for the desktop image
kp1, des1 = sift.detectAndCompute(img1, None)

# Connect to the device
adblib_test.adbclient_setup()
input_xy = (0, 0)


# Gets the x/y touch coordinates from the connected device
def get_device_xy():
    cmd = r'adb shell getevent'
    w = 0
    h = 0
    try:
        p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in p1.stdout:
            line = line.decode(encoding="utf-8", errors="ignore")
            line = line.strip()
            if ' 0035 ' in line:
                e = line.split(" ")
                w = e[3]
                w = int(w, 16)  # The output is hexadecimal, therefore base 16

            if ' 0036 ' in line:
                e = line.split(" ")
                h = e[3]
                h = int(h, 16)  # Same for H as for W
                if h > 0:
                    p = (w, h)
                    global input_xy
                    input_xy = p
        p1.wait()

        if cv.waitKey(1) == 27:  # ESC to kill thread
            p1.terminate()

    except Exception as e:
        print(f'Failed while getting input coordinates: {e}')


# Threaded function that feature-matches frames from screen and device capture
def process_last_frame(last_frame):

    last_frame = cv.cvtColor(last_frame, cv.COLOR_BGR2GRAY)     # Read in the last frame
    kp2, des2 = sift.detectAndCompute(last_frame, None)     # Detect features

    # Descriptor is empty when there are no features (picture is completely dark/black)
    if des2 is not None:

        # BFMatcher with default params
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []

        # If the distance is less than %
        for m, n in matches:
            if m.distance < BEST_IMAGE_PERCENTAGE*n.distance:
                good.append([m])

        kp1_good = []     # Keypoints that we are interested in

        for i in good:
            for x in i:
                kp1_good.append(kp1[x.queryIdx].pt)     # Sorted by ascending X coordinate value

        # Display rectangle only if detecting features
        if len(kp1_good) > 0:
            kp1_good_y = sorted(kp1_good, key=lambda x_val: x_val[-1])

            # Get edges
            global bot_right
            bot_right = (int(kp1_good[-1][0]), int(kp1_good_y[-1][1]))  # max(x) / max(y)
            global top_left
            top_left = (int(kp1_good[0][0]), int(kp1_good_y[0][1]))   # min(x) / min(y)


# Create a thread for listening to the input from the device
input_thread = threading.Thread(target=get_device_xy)
input_thread.start()

# Main loop
while True:

    current_frame = img1.copy()  # Copy the frame of the screen
    is_alive, frame = live_feed.read()  # Get frame from device's video feed

    if frame is not None:

        # If there are no current threads that are processing frames, we create a new one and start the processing
        if len(image_processing_threads) == 0:
            running_thread = threading.Thread(target=process_last_frame, args=(frame,))  # Start the thread
            running_thread.start()
            image_processing_threads.append(running_thread)  # Add to the list of threads which is used to keep track
        if top_left is not None or bot_right is not None:   # Check if there are coordinates from feature matching
            cv.rectangle(current_frame, top_left, bot_right, color, thickness)  # Draws a rectangle
    else:
        print('No frames detected')

    # If the image processing threads have finished, empty the list
    for thread in image_processing_threads:
        if not thread.is_alive():
            image_processing_threads = []

    cv.imshow('stream', current_frame)  # Show the screen
    print(input_xy)
    if cv.waitKey(1) == 27:    # ESC to exit
        break

cv.destroyAllWindows()
