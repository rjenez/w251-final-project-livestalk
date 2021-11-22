#!/bin/sh
rm -rf data
mkdir -p data
mkdir -p data/labelledimages
cd data/labelledimages

ROBOFLOWURL="https://app.roboflow.com/ds/gKCHZalU9J?key=0ZgC42DoXu"

curl -L $ROBOFLOWURL > roboflow.zip; unzip roboflow.zip; rm roboflow.zip
