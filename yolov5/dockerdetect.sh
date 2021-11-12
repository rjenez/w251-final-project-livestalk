#!/bin/bash
export DISPLAY=:0
source model_profile.sh

docker run --privileged --runtime nvidia --rm -e DISPLAY=$DISPLAY -v `pwd`:/usr/src/app/finalproject -v /tmp:/tmp --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/detectrtmp.sh  ${MODEL} ${IMAGE_SIZE}"

