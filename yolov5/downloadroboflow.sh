#!/bin/sh
mkdir -p data
mkdir -p data/labelledimages
cd data/labelledimages

ROBOFLOWURL="https://app.roboflow.com/ds/1BVTPMJlKz?key=rM1tht73Jq"

curl -L $ROBOFLOWURL > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
