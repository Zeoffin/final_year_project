# ORB Descriptors

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

desktop_image = "../Images/desktop.png"
region_image = "../Images/camera/4.jpg"

img1 = cv.imread(region_image, cv.IMREAD_GRAYSCALE)
img2 = cv.imread(desktop_image, cv.IMREAD_GRAYSCALE)

# Initiate ORB detector
orb = cv.ORB_create()
# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# create BFMatcher object
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
# Match descriptors.
matches = bf.match(des1, des2)
# Sort them in the order of their distance.
matches = sorted(matches, key=lambda x:x.distance)
# Draw first 10 matches.
img3 = cv.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.imshow(img3), plt.show()