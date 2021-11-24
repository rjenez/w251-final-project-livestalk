To set up messaging service

On edge device (text in arrows like `<text>` represents a parameter whose name can be changed:
  1. Build mqtt broker and file reader images by running the following in appropriate folders: 
      ```
      docker build -t mqtt_broker .
      docker build -t mqtt_message_forwarder .
      docker build -t file_reader .
      ```
  2. Create docker network (suggestion `mqtt`): 
      ```
      docker network create --driver bridge <network_name>
      ```
  3. Start mqtt broker container on created network with port 1883 mapped:
      ```
      docker run -d --name mqtt_broker --network <network_name> -p 1883:1883 mqtt_broker
      ```
  4. Start mqtt message forwarder container on network with the following arguments: 
      ```
      docker run -d --name mqtt_message_forwarder --network <network_name> mqtt_message_forwarder mqtt_broker <cloud_public_IP_address> <topic_name>
      ```
  5. Start mqtt file reader container that will read files from a specified directory and forward them through the pipeline: 
      ```
      docker run -d -v <path_of_folder_to_read_from>:/files --name file_reader --network <network_name> file_reader mqtt_broker <topic_name> /files
      ```
