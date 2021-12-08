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
For dockertrain.sh you will need to set the following in the environment file  model_profile.sh.
EPOCHS=50
IMAGE_SIZE=736
BATCH_SIZE=16
MODEL=yolov5s.pt
MODEL=yolov5m.pt
#MODEL=yolov5l.pt
#MODEL=yolov5x.pt
FREEZE=10
CONFIDENCE=0.45


Once the training is done, you may run detect by dockerdetect.sh on the images in the test set to see how well we did. You can look in the runs
directory after completing to see the outcome of the training and the results. This detection uses the weights generated in the training step which
is generally in {training output directory}/exp<number>/weights/best.pt. All of this handled so that you get the result of the last run in using the detect.sh script.
### Library to do individual image identification of cows
There is code in identify.py that implements a class that can be used to do in memory individual detection. It is the result of heavy modification of detect.py in yolov5. The library generates the annotated image with cows deteced, along with the locations of the detected cows in the image.

This library can be tested by running dockeridentify.sh

Files:
- [Readme.md](./Readme.md) This file with all the detail for setting up and running the training.
- [dockerbuildyolo.sh](./dockerbuildyolo.sh)) Build Docker container with yolov5 for nx
- [Dockerfile.yolov5](./Dockerfile.yolov5) Docker file for building yolov5 container
- [Dockerfile.yolov5mqtt](./Dockerfile.yolov5mqtt) Docker file for building yolov5 and mqtt in one container.
- [downloadroboflow.sh](./downloadroboflow.sh) Script to download image and label data from roboflow. Some configuration required.
- [train.sh](./train.sh) Shell script to invoke yolov5 training
- [dockertrain.sh](./dockertrain.sh) Run docker container to do training on images downloaded from training and validation.
- [dockerdetect.sh](./dockerdetect.sh) Run object detection on test images using docker
- [detect.sh](./detect.sh) Shell script to invoke yolov5 detection
- [dockeridentify.sh](./dockeridentify.sh) Run object identification on any image with docker
- [identify.sh](./identify.sh) Run object identification on any image
- [identify.py](./identify.py) Module to do in memory image identification and labeling of objects detected.
- [project.yaml](./project.yaml) Yaml file detail classes to detect and training and validation sets for train.sh.
- [model_profile.sh](./model_profile.sh) Environment variables that are set across traininging, detection and identification (sourced in the .sh files)
  
  

