_base_ = '../mmdetection/configs/yolox/yolox_tiny_8x8_300e_coco.py'

model = dict(bbox_head=dict(num_classes=1))

dataset_type = 'COCODataset'
classes = ('person',)
BASE_PATH='/home/zach/fiftyone/coco-2017/'
data = dict(
    samples_per_gpu=16,  # Batch size of a single GPU
    workers_per_gpu=8,  # Worker to pre-fetch data for each single GPU
    train=dict(
        dataset=dict(
            img_prefix=f'{BASE_PATH}train/data',
            classes=classes,
            ann_file=f'{BASE_PATH}train/labels.json'),
    ),
    val=dict(
        img_prefix=f'{BASE_PATH}validation/data',
        classes=classes,
        ann_file=f'{BASE_PATH}validation/labels.json'),
    test=dict(
        img_prefix=f'{BASE_PATH}validation/data',
        classes=classes,
        ann_file=f'{BASE_PATH}validation/labels.json'))
#TODO remove hardcoding
load_from = '/home/zach/Desktop/capstone/ISAC/deep-learning-training/checkpoints/yolox_tiny_8x8_300e_coco_20211124_171234-b4047906.pth'
