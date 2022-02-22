from PIL import ImageGrab
from image_processing import process_last_frame
from adblib import get_device_xy, adbclient_setup

import globals
import threading
import cv2 as cv
import numpy as np

# Constant values
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900
region_color = (255, 0, 0)  # Matched region color
region_thickness = 2        # Matched region line thickness

# Get the live feed from phone by using its IP address and app called 'IP Webcam'
url = "http://10.240.85.7:8080/video"
live_feed = cv.VideoCapture(url)

# Desktop image - to be replaced with live display capture
img1 = cv.imread("Images/desktop.png", cv.IMREAD_GRAYSCALE)

# Setup for stream
cv.namedWindow("stream", cv.WINDOW_NORMAL)
cv.resizeWindow("stream", WINDOW_WIDTH, WINDOW_HEIGHT)

# List for thread management
image_processing_threads = []

# Connect to the device
# adbclient_setup()

# Create a thread for listening to the input from the device
# input_thread = threading.Thread(target=get_device_xy)
# input_thread.start()

# Main loop
while True:

    # Get the display feed and convert it to numpy array
    display_frame = ImageGrab.grab(bbox=(0, 0, 1920, 1080))
    display_frame = np.array(display_frame)

    is_alive, video_frame = live_feed.read()  # Get frame from device's video feed

    if video_frame is not None:

        # If there are no current threads that are processing frames, we create a new one and start the processing
        if len(image_processing_threads) == 0:
            # TODO: Instead of threads, use multiprocessing
            running_thread = threading.Thread(target=process_last_frame, args=(video_frame, display_frame))
            running_thread.start()
            image_processing_threads.append(running_thread)  # Keep track of threads

        # Check for coordinates and draw a rectangle around the detected region
        if globals.TOP_LEFT_CORNER is not None or globals.BOT_RIGHT_CORNER is not None:
            cv.rectangle(display_frame, globals.TOP_LEFT_CORNER,
                         globals.BOT_RIGHT_CORNER, region_color, region_thickness)
    else:
        print('No frames detected')

    # If the image processing threads have finished, empty the list
    for thread in image_processing_threads:
        if not thread.is_alive():
            image_processing_threads = []

    display_frame = cv.cvtColor(display_frame, cv.COLOR_BGR2RGBA)
    cv.imshow('stream', display_frame)  # Show the screen
    # print(globals.INPUT_XY)
    if cv.waitKey(1) == 27:    # ESC to exit
        break

cv.destroyAllWindows()
