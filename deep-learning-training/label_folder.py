import cv2
from ultralytics import YOLO

model = YOLO('runs/detect/train/weights/best.pt')
x = model.predict('data/val/camera2_data_3_501.jpg', conf=.25)
print(x[0].boxes.boxes)

print(len(x[0].boxes.boxes))

