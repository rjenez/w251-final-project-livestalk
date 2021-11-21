#!/bin/bash
source ./model_profile.sh

docker run -e DISPLAY=$DISPLAY  -v /tmp/.X11-unix:/tmp/.X11-unix --privileged --runtime nvidia --rm -v `pwd`:/usr/src/app/finalproject --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/identify.sh ${IMAGE_SIZE} ${CONFIDENCE}"
