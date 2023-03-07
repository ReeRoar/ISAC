import cv2
import numpy as np
import os
# import requests
import urllib.request


# frame = None
# key = None
# count = 0


def image_frame(save_image=True):
    count = 0
    URL = "http://IP ADDRESS HERE/capture"
    if save_image:  # save_image=True
        try:
            if not os.path.exists('data'):
                os.makedirs('data')
        except OSError:
            print('Error: Creating path')

        while save_image:
            image_url = urllib.request.urlopen(URL)
            image_np = np.array(bytearray(image_url.read()), dtype=np.uint8)
            frame = cv2.imdecode(image_np, -1)
            #cv2.imshow('Display (Saving Frames)', frame)
            key = cv2.waitKey(500)
            name = "data/frame%d.jpg" % count
            cv2.imwrite(name, frame)  # save frame as JPG file
            count = count + 1
            print(count)
            #if key == (ord('q')):
        return frame
    else:
        #while not save_image:  # save_image=False
            image_url = urllib.request.urlopen(URL)
            image_np = np.array(bytearray(image_url.read()), dtype=np.uint8)
            frame = cv2.imdecode(image_np, -1)
            #cv2.imshow('Display (NOT Saving Frames)', frame)
            key = cv2.waitKey(500)
            #if key == (ord('q')):
            return frame


def main():
    i = 0
    key = cv2.waitKey(500)
    #while key != (ord('q')):
    while i < 1:
     test = image_frame(False)  # change either to (True) to save frames as images in a folder, or (False) to not save frames
     cv2.imshow('Image', test)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
