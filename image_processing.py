import cv2 as cv
import globals

sift = cv.SIFT_create()
BEST_IMAGE_PERCENTAGE = 0.4


# Threaded function that feature-matches frames from screen and device capture
def process_last_frame(last_frame, des1, kp1):
    """
    a generic description goes here
    :param last_frame:
    :param des1:
    :param kp1:
    """
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
            globals.BOT_RIGHT_CORNER = (int(kp1_good[-1][0]), int(kp1_good_y[-1][1]))  # max(x) / max(y)
            globals.TOP_LEFT_CORNER = (int(kp1_good[0][0]), int(kp1_good_y[0][1]))   # min(x) / min(y)
