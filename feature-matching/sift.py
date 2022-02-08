# SIFT
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.patches as patches

test_image = 16

img1 = cv.imread("../Images/desktop.png", cv.IMREAD_GRAYSCALE)           # queryImage
img2 = cv.imread("../Images/camera/" + str(test_image) + ".jpg", cv.IMREAD_GRAYSCALE)          # trainImage
# Initiate SIFT detector
sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
# Apply ratio test
good = []

# If the distance is less than %
for m,n in matches:
    if m.distance < 0.4*n.distance:
        good.append([m])

top_left, bot_left, bot_right, height, width = 0, 0, 0, 0, 0

kp1_good, kp2_good = [], []     # Keypoints that we are interested in

print(f'Length of good: {len(good)}')
for i in good:
    for x in i:
        kp1_good.append(kp1[x.queryIdx].pt)     # Sorted by ascending X coordinate value
print(f'Length of good kp1: {len(kp1_good)}')

# Sort the list by y value
kp1_good_y = sorted(kp1_good, key=lambda x_val: x_val[-1])

# Get edges
bot_left = (kp1_good[0][0], kp1_good_y[-1][1])    # min(x) / max(y)
bot_right = (kp1_good[-1][0], kp1_good_y[-1][1])  # max(x) / max(y)
top_left = (kp1_good[0][0], kp1_good_y[0][1])   # min(x) / min(y)

"""
    ---------------> x
    |
    |
    |
    v
    y
"""

width = bot_right[0] - bot_left[0]
height = top_left[1] - bot_left[1]

rows, columns = 2, 2

img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# TODO: Offest for the edges- add 50/100 px to W and H ?
rect = patches.Rectangle(bot_left, width, height, linewidth=1, edgecolor='r', facecolor='none')

fig, ax = plt.subplots(figsize=(20,10))
ax.imshow(img3)
ax.add_patch(rect)
plt.scatter(bot_left[0], bot_left[1], color='red')
plt.scatter(bot_right[0], bot_right[1], color='green')
plt.scatter(top_left[0], top_left[1], color='blue')
plt.show()
