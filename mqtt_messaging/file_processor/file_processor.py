import ast
import base64
import json
import paho.mqtt.client as mqtt
import pickle
import sys

from georeference_from_byte import get_exif
from map_ui import build_map

# Declare dataframe for tracking image and cow counts
df = pd.DataFrame()

# Set relevant variables for MQTT arguments
LOCAL_MQTT_HOST = sys.argv[1]
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = sys.argv[2]


# Declare method for subscribing to topic
def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)


# Method for handling new messages
def on_message(client, userdata, msg):
    try:
        global df
        print("got message")

        # Load json payload as JSON object
        data = json.loads(msg.payload)

        # Write original file to folder mapped to S3
        file_name = "var/www/s3/images/" + data["name"]
        image_data = base64.b64decode(data["bytes"].encode('utf-8'))
        with open(file_name, "wb") as binary_file:
            print(file_name)
            # Write bytes to file
            binary_file.write(image_data)

        # Write annotated image to folder mapped to S3
        annotated_image_data = base64.b64decode(data["annotated_bytes"].encode('utf-8'))
        with open("var/www/s3/annotated_images/" + data["name"], "wb") as binary_file:
            # Write bytes to file
            binary_file.write(annotated_image_data)
        print("done_writing")

        # Extract EXIF data from original image
        single_row_df = get_exif(image_data)

        # Append number of detected cows to df returned by previous method
        single_row_df["cow_count"] = data['count']

        # Update global df
        tmp = df.append(single_row_df)
        df = tmp

        # Log new dataframe
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(single_row_df)
            print("df")
            print(df)

        # Build new map with updated df
        build_map(df, img_dir="https://251bucket.s3.us-east-2.amazonaws.com/annotated_images/")


    except:
        print("Unexpected error:", sys.exc_info()[0])


local_mqtt_client = mqtt.Client()
local_mqtt_client.on_connect = on_connect_local
local_mqtt_client.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 36000)
local_mqtt_client.on_message = on_message

# go into a loop
local_mqtt_client.loop_forever()
