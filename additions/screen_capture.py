import PIL.features
import numpy as np
import cv2 as cv
from PIL import ImageGrab

cv.namedWindow("stream", cv.WINDOW_NORMAL)
cv.resizeWindow('stream', 1000, 800)

while True:
    img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))  # x, y, w, h  | If set to None, will capture all screens
    img_np = np.array(img)
    frame = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
    cv.imshow("stream", frame)
    if cv.waitKey(1) & 0Xff == ord('q'):
        break

cv.destroyAllWindows()
