#!/bin/sh
docker run --privileged --runtime nvidia --rm -v `pwd`:/usr/src/app/finalproject --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/trainanddetect.sh 416 16 10 yolov5s.pt"
