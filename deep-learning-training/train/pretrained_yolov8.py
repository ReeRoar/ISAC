from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data="/home/zach/fiftyone/coco-2017/person_coco.yaml", epochs=100, imgsz=640,patience=2)