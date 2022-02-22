from timing import Timer

import cv2 as cv
import globals

sift = cv.SIFT_create()
BEST_IMAGE_PERCENTAGE = 0.4

timer = Timer()


def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)

    return cv.resize(frame, dim, interpolation=cv.INTER_AREA)


# Threaded function that feature-matches frames from screen and device capture
def process_last_frame(video_frame, display_frame):
    """
    a generic description goes here
    :param video_frame:
    :param display_frame:
    """

    video_frame = cv.cvtColor(video_frame, cv.COLOR_BGR2GRAY)  # Read in the last frame
    display_frame = cv.cvtColor(display_frame, cv.COLOR_BGR2GRAY)

    timer.start()

    # Reduce the resolution
    video_frame = rescale_frame(video_frame)
    display_frame = rescale_frame(display_frame)

    # TODO: This bit is slow af
    kp1, des1 = sift.detectAndCompute(display_frame, None)
    kp2, des2 = sift.detectAndCompute(video_frame, None)  # Detect features

    timer.stop()

    # Descriptor is empty when there are no features (picture is completely dark/black)
    if des2 is not None:

        # BFMatcher with default params
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # Apply ratio test
        good = []

        # If the distance is less than %
        for m, n in matches:
            if m.distance < BEST_IMAGE_PERCENTAGE * n.distance:
                good.append([m])

        kp1_good = []  # Keypoints that we are interested in

        for i in good:
            for x in i:
                kp1_good.append(kp1[x.queryIdx].pt)  # Sorted by ascending X coordinate value

        # Display rectangle only if detecting features
        if len(kp1_good) > 0:
            kp1_good_y = sorted(kp1_good, key=lambda x_val: x_val[-1])

            # Get edges
            globals.BOT_RIGHT_CORNER = (int(kp1_good[-1][0]), int(kp1_good_y[-1][1]))  # max(x) / max(y)
            globals.TOP_LEFT_CORNER = (int(kp1_good[0][0]), int(kp1_good_y[0][1]))  # min(x) / min(y)
