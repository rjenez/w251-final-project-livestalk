# w251-final-project-livestalk
This the code repo for W251 final project, Livestalk, using drones to count cattle (livestock).
The process involves training image detection for cows in the field, via video from a drone.
Once this is done, we can fly a drone and get live streams and count cows in the field as
the drone flies with real time updates being shown on a map.

Files:
- [Readme.md](./Readme.md) This file with all the detail for setting up and running the training
- [rtmp](./rtmp) Directory containing the RTMP server container to get live video streams
- [yolov5](./yolov5) Directory containing the Yolov5 container, training scripts and object detect using yolov5 for the RTMP stream from the drone
- [test_map](./test_map) Directory containing the imagery field of view calculator, image exif and xml parser, and map generation script used to generate the final UI
