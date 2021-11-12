#!/bin/sh

export PYTHONIOENCODING=utf-8

python3 detect.py --weights runs/train/exp/weights/best.pt --img $1 --conf $2 --project /usr/src/app/finalproject/runs/detect --source /usr/src/app/finalproject/data/labelledimages/test/images

