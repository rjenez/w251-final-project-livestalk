# w251-final-project-livestalk
This is the code repo for Team Livestalk's W251 Fall 2021 final project. The Livestalk project uses drones to detect and count cattle (livestock) and renders the information onto a real-time map for ranchers.
The process involves training an object detection model for cows on a field or pasture from video frames.
Once the model is trained, we can fly a drone, perform inference on a Jetson edge device mounted to a drone, and stream annotated images and count cows onto a map so that ranchers can take stock (no pun intended) of their livestock in realtime.

Files:
- [Readme.md](./Readme.md) This file with all the detail for setting up and running the training
- [rtmp](./rtmp) Directory containing the RTMP server container to get live video streams
- [yolov5](./yolov5) Directory containing the Yolov5 container, training scripts and object detect using yolov5 for the RTMP stream from the drone
- [test_map](./test_map) Directory containing the imagery field of view calculator, image exif and xml parser, and map generation script used to generate the final UI
