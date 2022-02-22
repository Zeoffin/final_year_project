
from PIL import ImageGrab
from image_processing import process_last_frame
from adblib import get_device_xy, adbclient_setup

import globals
import threading
import cv2 as cv

# Constants
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900

# Get the live feed from phone by using its IP address and app called 'IP Webcam'
url = "http://10.240.85.7:8080/video"
live_feed = cv.VideoCapture(url)

# Desktop image - to be replaced with live display capture
img1 = cv.imread("Images/desktop.png", cv.IMREAD_GRAYSCALE)

# Setup for stream
cv.namedWindow("stream", cv.WINDOW_NORMAL)
cv.resizeWindow("stream", WINDOW_WIDTH, WINDOW_HEIGHT)

# List for thread For threading management
image_processing_threads = []

# Parameters for drawing the matched region
region_color = (255, 0, 0)
region_thickness = 2

# Initiate SIFT detector
sift = cv.SIFT_create()

# Find the keypoints for the desktop image
kp1, des1 = sift.detectAndCompute(img1, None)

# Connect to the device
# adbclient_setup()

# Create a thread for listening to the input from the device
# input_thread = threading.Thread(target=get_device_xy)
# input_thread.start()

# Main loop
while True:

    current_frame = img1.copy()  # Copy the frame of the screen
    is_alive, frame = live_feed.read()  # Get frame from device's video feed

    if frame is not None:

        # If there are no current threads that are processing frames, we create a new one and start the processing
        if len(image_processing_threads) == 0:
            running_thread = threading.Thread(target=process_last_frame, args=(frame, des1, kp1))  # Start the thread
            running_thread.start()
            image_processing_threads.append(running_thread)  # Add to the list of threads which is used to keep track

        # Check for coordinates and draw a rectangle around the detected region
        if globals.TOP_LEFT_CORNER is not None or globals.BOT_RIGHT_CORNER is not None:
            cv.rectangle(current_frame, globals.TOP_LEFT_CORNER,
                         globals.BOT_RIGHT_CORNER, region_color, region_thickness)
    else:
        print('No frames detected')

    # If the image processing threads have finished, empty the list
    for thread in image_processing_threads:
        if not thread.is_alive():
            image_processing_threads = []

    cv.imshow('stream', current_frame)  # Show the screen
    # print(globals.INPUT_XY)
    if cv.waitKey(1) == 27:    # ESC to exit
        break

cv.destroyAllWindows()
