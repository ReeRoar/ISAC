import cv2
import numpy as np
import os
# import requests
import urllib.request

count = 0
while True:
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print('Error: Creating path')

    image_url = urllib.request.urlopen('IP ADDRESS HERE/capture')
    image_np = np.array(bytearray(image_url.read()), dtype=np.uint8)
    frame = cv2.imdecode(image_np, -1)
    cv2.imshow('Display', frame)
    key = cv2.waitKey(500)
    name = "data/frame%d.jpg" % count
    cv2.imwrite(name, frame)  # save frame as JPEG file
    count += 1
    if key == (ord('q')):
        break