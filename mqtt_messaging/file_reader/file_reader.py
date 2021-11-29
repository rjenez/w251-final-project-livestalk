import numpy as np
import cv2 as cv
import paho.mqtt.client as mqtt
import sys
import time
import json
from watchdog.observers import Observer
import pickle
import base64
from watchdog.events import FileSystemEventHandler

LOCAL_MQTT_HOST=sys.argv[1]
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC = sys.argv[2]
FILE_DIRECTORY = sys.argv[3]

class Watcher:
    DIRECTORY_TO_WATCH = "/path/to/my/directory"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        print("trying to connect")
        local_mqttclient = mqtt.Client()
        #local_mqttclient.on_connect = on_connect_local
        #local_mqttclient.on_disconnect=on_disconnect_local
        local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 3600)
        event_handler = Handler(local_mqttclient)
        #event_handler = Handler()
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
            # Take any action here when a file is first created.
            print("Received modified event - %s." % event.src_path)
            with open(event.src_path, 'rb') as f:
               # file_bytes =f.read()
                bytes_str = base64.b64encode(f.read()).decode('utf-8')
                #print(bytes_str)
                if bytes_str:
                    print('in')
                    json_object = {"name" : event.src_path, "bytes" : "test"}
                    json_string = json.dumps(json_object)
               # pickle_string = str(pickle.dumps(json_object))
               # prit(pickle_string)
                    #self.mqtt_client.publish(LOCAL_MQTT_TOPIC, "test")
                    self.mqtt_client.publish(LOCAL_MQTT_TOPIC, json_string)


        elif event.event_type == 'created':
            # Taken any action here when a file is modified.
            print("Received created event - %s." % event.src_path)

# def on_connect_local(client, userdata, flags, rc):
#     print("connected to local broker with rc: " + str(rc))
#
# def on_disconnect_local(client, userdata, rc):
#     print("disconnecting reason  "  +str(rc))

#print("trying to connect")
# local_mqttclient = mqtt.Client()
# local_mqttclient.on_connect = on_connect_local
# local_mqttclient.on_disconnect=on_disconnect_local
# local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
w = Watcher()
w.run()
