## Training and Object Detection Using Yolov5

### Building yolov5 container
You may build an appropriate yolov5 container by executing the script dockerbuildyolo.sh. It uses the Dockerfile.yolov5
docker file. 

### Training
#### Download Images
You can train the datasets from roboflow by first downloading the images and labels. Please use the script downloadroboflow.sh, which
will download the roboflow images and labels to the right places for the next step in doing our training. You will need to have
the URL from roboflow that specfies the location of the project. Please set the environment variable ROBOFLOWURL with this link.
It should look like "https://app.roboflow.com/ds/1BVTPMJlKz?key=rM1tht73Jq" (export ROBOFLOWURL="https://app.roboflow.com/ds/1BVTPMJlKz?key=rM1tht73Jq").
#### Execute Training (and detection)
Once the images are downloaded the next step is to execute training. You make execute the dockerrun.sh script that does training and detection.
You will need to update project.yaml that has the details for classes we want to use and specifics for where the images are (should be all set if you
use the downloadroboflow.sh.
For dockerrun.sh you will need to set the following environment variables (or use the defaults in the script).
EPOCHS=10
IMAGE_SIZE=416
BATCH_SIZE=16
MODEL=yolov5s.pt

Once the training is done, it will automatically do a detection run on the images in the test set to see how well we did. You can look in the runs
directory after completing to see the outcome of the training and the results.
### Image detection through rtmp
Once we have the model trained, we can execute the dockerdetect.sh script which starts readiding the rtmp stream rtmp://<rtmp_server_ip>/live/livestalk.
You will need to set the RTMPSRC environment variable to specificy this source before executed the detection script.
***Note, you will need to have established a stream before starting the run this script (Need to find out why that is).
The results of the detection of the images will be put in the directtory runs/detect/exp<n>/. There will be a livestalk.mp4 file with the vidoe
of the stream with detected images. Along with this there is a labels directory that has a file livestalk_xxx.txt which has every has
boounding box data for every image detected. The number of lines corresponds to the number of objects detected in each frame.

This file data can be used to stich together the number of cows detected.

Files:
- [Readme.md](./Readme.md) This file with all the detail for setting up and running the training.
- [dockerbuildyolo.sh](./dockerbuildyolo.sh)) Build Docker container with yolov5 for nx
- [Dockerfile.yolov5](./Dockerfile.yolov5) Docker file for building yolov5
- [downloadroboflow.sh](./downloadroboflow.sh) Script to download image and label data from roboflow. Some configuration required.
- [dockerrun.sh](./dockerrun.sh) Run docker container to do training and detection of the images.
- [dockerdetect.sh](./dockerdetect.sh) Run object detection pipeline using rtmp video feed we receive from the drone

