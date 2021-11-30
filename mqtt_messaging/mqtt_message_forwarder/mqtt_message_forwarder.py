import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sys
import json
import time

arguments = sys.argv

LOCAL_MQTT_HOST=sys.argv[1]
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC=sys.argv[3]

REMOTE_MQTT_HOST=sys.argv[2]
REMOTE_MQTT_PORT=1883
REMOTE_MQTT_TOPIC=sys.argv[3]

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  try:
    # if we wanted to re-publish this message, something like this should work
    data = json.loads(msg.payload)
    print(data['name'])
    publish.single(REMOTE_MQTT_TOPIC, msg.payload, qos=1, hostname=REMOTE_MQTT_HOST)
    # remote_mqttclient = mqtt.Client()
    # remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 60)
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg.payload, qos=1, retain=False)
    time.sleep(1)
    print("sent")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 36000)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()

