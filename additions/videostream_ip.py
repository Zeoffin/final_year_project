"""
This is code for processing video stream from phone by using 'IP Webcam' app
"""

import requests
import cv2
import numpy as np

# Subject to change every time
url = "http://10.240.85.7:8080/shot.jpg"

cv2.namedWindow("stream", cv2.WINDOW_NORMAL)
cv2.resizeWindow("stream", 900, 600)

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)

    #cv2.rectangle(img, (2, 2), (300, 600), (255, 0, 0), 2)  # Draws a rectangle

    cv2.imshow("stream", img)

    if cv2.waitKey(1) == 27:    # ESC to exit
        break