#!/bin/sh

export PYTHONIOENCODING=utf-8

lastexp=`ls -At /usr/src/app/finalproject/runs/train | head -1`
weightfile="/usr/src/app/finalproject/runs/train/${lastexp}/weights/best.pt"
python3 /usr/src/app/finalproject/identify.py --weights $weightfile --source /usr/src/app/finalproject/data/labelledimages/test/images --view-img

