# RTMP Streaming on Nx/Nano
### Run RTMP Streaming

You all can try this by doing a pull and executing (dockerbuildrtmp.sh) to the build for your platform , then run dockerrunrtmp.sh to get the rtmp server up and running
(you can stop it by running dockerstoprtmp.sh). For all you iphone folks get Larix from the app store and broadcast on a stream of rtmp://\<your ip\>/live/livestalk.
You can download VLC and create a network that listens for video broadcast on this rtmp stream.

Files:
- [Readme.md](./Readme.md) This file with all the detail for setting up and running the training.
- [dockerbuildrtmp.sh](./dockerbuildrtmp.sh) Buildi Docker container with rtmp for nx
- [Dockerfile.rtmp](./Dockerfile.rtmp) Docker file for building rtmp
- [nginx.conf](./nginx.conf) nginx.conf used for configuring the nginx instance with rtmp server
- [dockerrunrtmp.sh](./dockerrunrtmp.sh) Run docker container with rtmp server
- [dockerstoprtmp.sh](./dockerstoprtmp.sh)d Stop and remove docker container with rtmp server



