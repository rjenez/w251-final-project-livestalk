#!/bin/bash
source ./model_profile.sh

docker run --privileged --runtime nvidia --rm -v `pwd`:/usr/src/app/finalproject --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/trainanddetect.sh ${IMAGE_SIZE} ${BATCH_SIZE} ${EPOCHS} ${MODEL} ${FREEZE}"
