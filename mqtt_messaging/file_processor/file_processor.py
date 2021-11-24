import paho.mqtt.client as mqtt
import sys
import pickle
import ast

LOCAL_MQTT_HOST=sys.argv[1]
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC=sys.argv[2]

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC)
	
def on_message(client,userdata, msg):
  #try:
    
    # if we wanted to re-publish this message, something like this should work
    # msg = msg.payload
    # remote_mqttclient.publish(REMOTE_MQTT_TOPIC, payload=msg, qos=0, retain=False)
    #data = pickle.loads(ast.literal_eval(msg.payload))
    #print(data)
    with open("var/www/s3/my_file.JPG", "wb") as binary_file:
        print(msg.payload)
    # Write bytes to file
        binary_file.write(msg.payload)
  #except:
   # print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message



# go into a loop
local_mqttclient.loop_forever()
