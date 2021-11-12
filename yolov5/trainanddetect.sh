#!/bin/sh

export PYTHONIOENCODING=utf-8

python3 train.py --img $1 --batch $2 --epochs $3 --data /usr/src/app/finalproject/project.yaml --weights $4 --freeze $5 --cache
python3 detect.py --weights runs/train/exp/weights/best.pt --img $1 --conf 0.90 --project /usr/src/app/finalproject/runs/detect --source /usr/src/app/finalproject/data/labelledimages/test/images

