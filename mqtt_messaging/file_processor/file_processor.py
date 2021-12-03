import paho.mqtt.client as mqtt
import sys
import pickle
import ast
import json
import base64
import pandas as pd

import sys
from georeference_from_byte import get_exif
from map_ui import build_map


df = pd.DataFrame()

LOCAL_MQTT_HOST=sys.argv[1]
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC=sys.argv[2]

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  #try:
    global df
    # if we wanted to re-publish this message, something like this should work
    # msg = msg.payload
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    print("got message")
    data = json.loads(msg.payload)
    file_name = "var/www/s3/images/" + data["name"]
    image_data = base64.b64decode(data["bytes"].encode('utf-8'))
    #print(data)
    with open(file_name, "wb") as binary_file:
        print(file_name)
    # Write bytes to file
        binary_file.write(image_data)


    annotated_image_data =  base64.b64decode(data["annotated_bytes"].encode('utf-8'))
# print(data)
    with open("var/www/s3/annotated_images/" + data["name"], "wb") as binary_file:
    # Write bytes to file
        binary_file.write(annotated_image_data)
        print("done_writing")


    single_row_df = get_exif(image_data)
    single_row_df["cow_count"] = data['count']
    tmp = df.append(single_row_df)
    df = tmp
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(single_row_df)
        print("df")
        print(df)
    build_map(df, img_dir="https://251bucket.s3.us-east-2.amazonaws.com/annotated_images/")
  #except:
   # print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 36000)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()
