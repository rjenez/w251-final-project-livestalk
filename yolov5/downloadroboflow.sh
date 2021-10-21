#!/bin/sh
mkdir -p data
mkdir -p data/labelledimages
cd data/labelledimages
curl -L "https://app.roboflow.com/ds/1BVTPMJlKz?key=rM1tht73Jq" > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
