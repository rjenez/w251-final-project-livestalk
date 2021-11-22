#!/bin/sh

export PYTHONIOENCODING=utf-8
#conf_thres=0.3, iou_thres=0.45, max_det=1000, device=, view_img=False, save_txt=False, save_conf=False, save_crop=False, nosave=False, classes=None, agnostic_nms=False, augment=False, visualize=False, update=False, project=/usr/src/app/finalproject/runs/detect, name=exp, exist_ok=False, line_thickness=3, hide_labels=False, hide_conf=False, half=False, dnn=False

lastexp=`ls -At /usr/src/app/finalproject/runs/train | head -1`
weightfile="/usr/src/app/finalproject/runs/train/${lastexp}/weights/best.pt"

python3 detect.py --weights $weightfile --img $1 --conf $2 --project /usr/src/app/finalproject/runs/detect --source /usr/src/app/finalproject/data/labelledimages/test/images --save-txt --save-crop

