from ultralytics import YOLO

model = YOLO('runs/detect/train2/weights/last.pt')
model.train(data="/home/zach/fiftyone/coco-2017/person_coco.yaml", epochs=100, imgsz=640,patience=5, optimizer='AdamW', lr0=0.0001,lrf=0.0001,cos_lr=True)