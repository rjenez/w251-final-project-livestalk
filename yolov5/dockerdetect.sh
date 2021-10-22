#!/bin/sh
export DISPLAY=:0
docker run --privileged --runtime nvidia --rm -e DISPLAY=$DISPLAY -v `pwd`:/usr/src/app/finalproject -v /tmp:/tmp --ipc=host --gpus all -ti yolov5 bash -c "../finalproject/detectrtmp.sh yolov5s.pt 416"
#docker run --privileged --runtime nvidia --rm -v /data:/data -e DISPLAY -v /tmp:/tmp -ti yolov5 python3 detect.py --source rtmp://192.168.4.1/live/1234 --weights yolov5x.pt --conf 0.4


#../finalproject/face_detection_yolov5s.pt 416"
