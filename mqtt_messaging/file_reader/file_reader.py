import base64
import cv2 as cv
import json
import numpy as np
import paho.mqtt.client as mqtt
import pickle
import sys
import time

from identify import identify, parse_opt
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Set variables for connecting to MQTT
LOCAL_MQTT_HOST = "mqtt_broker"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "topic"
FILE_DIRECTORY = "/files"


class Watcher:

    def __init__(self):
        self.observer = Observer()

    def run(self):
        print("trying to connect")

        # Create MQTT Client and pass to event handler for sending data
        # to MQTT
        local_mqtt_client = mqtt.Client()
        local_mqtt_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 36000)
        event_handler = Handler(local_mqtt_client)
        self.observer.schedule(event_handler, FILE_DIRECTORY, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def on_any_event(self, event):
        if event.is_directory:
            return None

        elif event.event_type == 'modified':
            print("Received modified event - %s." % event.src_path)


        elif event.event_type == 'created':
            # Taken any action here when a file is modified.
            print("Received created event - %s." % event.src_path)
            with open(event.src_path, 'rb') as f:
                # Read original byte data and convert to string
                bytes = f.read()
                bytes_str = base64.b64encode(bytes).decode('utf-8')

                # Set arguments for running YOLOV5 object detection
                opt = parse_opt()
                opt.weights = ['/yolov5/best.pt']
                opt.conf_thres = [0.45]

                # Run detection
                id = identify(**vars(opt))
                image, labels = id.detect(bytes, conf_thres=0.45)
                print(' '.join(labels))

                # Read labeled image and covnert to string
                annotated_bytes_str = base64.b64encode(image).decode('utf-8')

                # As long as original image is not empty
                if bytes_str:
                    print('in')

                    # Generate json string and send to MQTT broker
                    base_file_name = event.src_path.rsplit('/', 1)[-1]
                    json_object = {"name": base_file_name, "bytes": bytes_str, "annotated_bytes": annotated_bytes_str,
                                   "count": len(labels)}
                    json_string = json.dumps(json_object)
                    self.mqtt_client.publish(LOCAL_MQTT_TOPIC, json_string)


w = Watcher()
w.run()
