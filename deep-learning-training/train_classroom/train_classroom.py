from ultralytics import YOLO


model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)
model.train(data='/home/zach/Desktop/capstone/ISAC/deep-learning-training/data/data.yaml', epochs=400,
            imgsz=340, batch=-1, patience=5, lr0=0.001)
#model.train(data='/home/zach/Desktop/capstone/ISAC/deep-learning-training/data/data.yaml', epochs=400, imgsz=640, batch=-1, patience=5, lr0=0.001)