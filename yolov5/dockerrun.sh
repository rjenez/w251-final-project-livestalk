#!/bin/sh
EPOCHS=10
IMAGE_SIZE=416
BATCH_SIZE=16
MODEL=yolov5s.pt

docker run --privileged --runtime nvidia --rm -v `pwd`:/usr/src/app/finalproject --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/trainanddetect.sh ${IMAGE_SIZE} ${BATCH_SIZE} ${EPOCHS} ${MODEL}"
