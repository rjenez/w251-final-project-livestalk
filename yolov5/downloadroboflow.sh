#!/bin/sh
rm -rf data
mkdir -p data
mkdir -p data/labelledimages
cd data/labelledimages

ROBOFLOWURL="https://app.roboflow.com/ds/OHzwf3QUxn?key=17aE2fjUOq"

curl -L $ROBOFLOWURL > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
