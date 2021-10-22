#!/bin/sh

export PYTHONIOENCODING=utf-8

RTMPSRC=rtmp://192.168.4.159/live/livestalk
python3 detect.py --weights $1  --conf 0.40 --source $RTMPSRC --project /usr/src/app/finalproject/runs/detect --save-txt --save-conf

