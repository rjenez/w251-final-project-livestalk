!/bin/bash

mkdir -p data

for file in videos/2021-*.mp4; do
    destination="data/output${file:12:${#file}-17}";
    mkdir -p "$destination";
    ffmpeg -i "$file" -r 0.25 "$destination/image-%d.jpeg";
done
