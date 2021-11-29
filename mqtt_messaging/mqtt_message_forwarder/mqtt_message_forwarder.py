import paho.mqtt.client as mqtt
import sys
import json

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
    remote_mqttclient = mqtt.Client()
    remote_mqttclient.connect(REMOTE_MQTT_HOST, REMOTE_MQTT_PORT, 36000)
    remote_mqttclient.publish(REMOTE_MQTT_TOPIC, REMOTE_MQTT_TOPIC, payload=msg.payload, qos=0, retain=False)
    print("sent")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 36000)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()

