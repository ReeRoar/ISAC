import fiftyone.zoo as foz
import torch
import fiftyone.utils.coco as fouc
from PIL import Image


def load_coco_dataset(split: str, overwrite: bool = False):
    """
    Loads in microsoft COCO dataset from fiftyone
    :param split: Split of data. Must be train or validation
    :param overwrite: boolean value representing whether to overwrite existing files
    :return: loaded in dataset
    """
    try:
        data = foz.load_zoo_dataset(
            "coco-2017",
            split=split,
            classes=["person", ],
            only_matching=True,
            overwrite=overwrite
        )
        return data
    except:
        return load_coco_dataset(split, overwrite)

