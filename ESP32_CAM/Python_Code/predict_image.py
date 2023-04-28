from ultralytics import YOLO
import cv2
import requests

IP = '127.0.0.1'
PORT = '5000'
base_url = f'http://{IP}:{PORT}/attendance_count/1'
model = YOLO('best.pt')


def pred_img(image, model=model, conf=.11):
    x = model.predict(image, conf=conf, verbose=False)
    return len(x[0].boxes.boxes)


def crop_img(img,crop=(None,None,None,None)):
    img = cv2.imread(img)
    cropped_image = img[crop[0]:crop[1], crop[2]:crop[3]]
    return cropped_image


def two_image_result(image1,image2, crop1=(None,None,None,None), crop2=(None,None,None,None)):
    cropped_img1 = crop_img(image1,crop1)
    results1 = pred_img(cropped_img1)
    cropped_img2 = crop_img(image2,crop2)
    results2 = pred_img(cropped_img2)
    requests.put(base_url,json={'camera_value':results1+results2})




#print(pred_img(crop_img('frame2494_2.jpg',(150,None,150,None)))) #150, 150 default for d316 camera 3
