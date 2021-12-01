import os
from create_annotations import *
import cv2
import argparse
import glob
import json
import numpy as np


def images_annotations_info(opt):
    label_path = None
    annotations = []
    images = []
    # Make sure to change the image extension
    img_paths = glob.glob(f"{opt.image}/*{opt.extension}")

    image_id = 0
    annotation_id = 1  # In COCO dataset format, you must start annotation id with 1

    for img in img_paths:
        if image_id % 100 == 0:
            print(f"Processing {str(image_id)}...")

        img_file = cv2.imread(img)

        h, w, _ = img_file.shape
        score = None

        image = create_image_annotation(img, w, h, image_id)
        images.append(image)

        if opt.labels == 'act':
            label_path = img.replace('images', 'labels_act').replace(f'.{opt.extension}', '.txt')
        elif opt.labels == 'pred':
            label_path = img.replace('images', 'labels_pred').replace(f'.{opt.extension}', '.txt')

        if os.path.exists(label_path):
            with open(label_path, "r") as label_file:
                label_read_line = label_file.readlines()
            # yolo format - (class_id, x_center, y_center, width, height)
            # coco format - (annotation_id, x_upper_left, y_upper_left, width, height)
            for line1 in label_read_line:
                label_line = line1
                category_id = int(label_line.split()[0]) + 1  # you start with annotation id with '1'
                x_center = float(label_line.split()[1])
                y_center = float(label_line.split()[2])
                width = float(label_line.split()[3])
                height = float(label_line.split()[4])

                if len(label_line.split()) > 5:
                    score = float(label_line.split()[5])
                int_x_center = int(img_file.shape[1] * x_center)
                int_y_center = int(img_file.shape[0] * y_center)
                int_width = int(img_file.shape[1] * width)
                int_height = int(img_file.shape[0] * height)

                min_x = int_x_center - int_width / 2
                min_y = int_y_center - int_height / 2
                width = int_width
                height = int_height

                annotation = create_annotation_yolo_format(min_x, min_y, width, height, image_id, category_id,
                                                           annotation_id, score)
                annotations.append(annotation)
                annotation_id += 1

        image_id += 1

    return images, annotations


def get_args():
    parser = argparse.ArgumentParser('Yolo format annotations to COCO dataset format')
    parser.add_argument('-i', '--image', type=str, help='Absolute path for images')
    parser.add_argument('-c', '--classes', type=str, help="Absolute path for classes")
    parser.add_argument('-l', '--labels', type=str, default="act", choices=['act', 'pred'],
                        help='Which folder to get object labels from')
    parser.add_argument('-e', '--extension', type=str, default="png", choices=['png', 'jpg'],
                        help='Choose the image extension')
    parser.add_argument('-o', '--output', type=str, help='Name the output json file')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    opt = get_args()
    output_name = opt.output
    output_path = f"output/{output_name}.json"
    classes = []

    with open(opt.classes, "r") as f:
        lines = f.readlines()
        for line in lines:
            name = line.strip()
            classes.append(name)

    print("Start!")
    coco_format['images'], coco_format['annotations'] = images_annotations_info(opt)

    for index, label in enumerate(classes):
        ann = {
            "supercategory": "Disinfect_5obj",
            "id": index + 1,  # Index starts with '1' .
            "name": label
        }
        coco_format['categories'].append(ann)

    with open(output_path, 'w') as outfile:
        json.dump(coco_format, outfile)

    print("Finished!")
