FROM ubuntu
  
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install paho-mqtt
RUN pip3 install Cython
RUN pip3 install numpy
RUN pip3 install watchdog
# example from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
COPY /file_reader/file_reader.py file_reader.py
#COPY haarcascade_frontalface_default.xml haarcascade_frontalface_default.xml
RUN mkdir /files
ENTRYPOINT ["python3","-u", "file_reader.py"]
