#!/bin/sh
export DISPLAY=:0
docker run --privileged --runtime nvidia --rm -e DISPLAY=$DISPLAY -v `pwd`:/usr/src/app/finalproject -v /tmp:/tmp --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/detectrtmp.sh yolov5s.pt 416"

