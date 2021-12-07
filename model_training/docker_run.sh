#!/bin/sh
sudo docker run --privileged --rm -v `pwd`:/usr/src/app/ -p 8889:8888 --ipc=host --gpus all model_training
#once run, access with http://localhost:8889/lab from outside container
