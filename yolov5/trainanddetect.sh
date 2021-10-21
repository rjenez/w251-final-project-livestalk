#!/bin/sh

export PYTHONIOENCODING=utf-8

python3 train.py --img $1 --batch $2 --epochs $3 --data /usr/src/app/finalproject/project.yaml --weights $4 --cache
python3 detect.py --weights runs/train/exp/weights/best.pt --img $1 --conf 0.90 --source ../finalproject/data/labelledimages/test/images
rm -rf ../finalproject/runs
cp -r runs ../finalproject/
