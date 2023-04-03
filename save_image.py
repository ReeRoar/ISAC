import cv2
import numpy as np
import os
# import requests
import urllib.request

folder_name = 'data_train5'
cam_path1 = folder_name + '/camera'
cam_path2 = folder_name + '/camera2'
cam_path3 = folder_name + '/camera3'
count = 0

while True:
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name + '/camera')
            os.makedirs(folder_name + '/camera2')
            os.makedirs(folder_name + '/camera3')
    except OSError:
        print('Error: Creating path')

    image_url = urllib.request.urlopen('http://192.168.1.101/capture') #linksys -192.168.1.101
    image_np = np.array(bytearray(image_url.read()), dtype=np.uint8)
    frame = cv2.imdecode(image_np, -1)
    image_url2 = urllib.request.urlopen('http://192.168.1.102/capture') #linksys -http://192.168.1.102
    image_np2 = np.array(bytearray(image_url2.read()), dtype=np.uint8)
   # image_url3 = urllib.request.urlopen('http://192.168.1.103/capture') #linksys 192.168.1.103
   # image_np3 = np.array(bytearray(image_url3.read()), dtype=np.uint8)
    frame2 = cv2.imdecode(image_np2, -1)
   # frame3 = cv2.imdecode(image_np3, -1)
    cv2.imshow('Display', frame)
    cv2.imshow('Display2', frame2)
   # cv2.imshow('Display3', frame3)
    key = cv2.waitKey(500)
    name = cam_path1 + '/frame%d.jpg' % count
    name2 = cam_path2 + '/frame%d.jpg' % count
   # name3 = cam_path3 + '/frame%d.jpg' % count
    cv2.imwrite(name, frame)  # save frame as JPEG file
    cv2.imwrite(name2, frame2)
   # cv2.imwrite(name3, frame3)
    count += 1
    if key == (ord('q')):
        break
