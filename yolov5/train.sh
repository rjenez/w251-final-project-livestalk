#!/bin/sh

export PYTHONIOENCODING=utf-8

python3 train.py --img $1 --batch $2 --epochs $3 --data /usr/src/app/finalproject/project.yaml --project /usr/src/app/finalproject/runs/train  --weights $4 --freeze $5 --cache

