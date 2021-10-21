!/bin/bash

mkdir -p data
mkdir -p data/images

for file in videos/2021-*.mp4; do
    ffmpeg -i "$file" -r 0.25 "data/images/image-`date +%d-%m-%Y-%H:%M:%S`%d.jpg";
done
