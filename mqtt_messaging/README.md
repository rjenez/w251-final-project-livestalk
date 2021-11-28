To set up messaging service

On edge device (text in arrows like `<text>` represents a parameter whose name can be changed):
  1. Build mqtt broker and file reader images by running the following in this directory: 
      ```
      docker build -t mqtt_broker -f /mqtt_broker/Dockerfile .
      docker build -t mqtt_message_forwarder -f /mqtt_message_forwarder/Dockerfile .
      docker build -t file_reader -f /file_reader/Dockerfile .
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

On cloud device:
  1. Build mqtt broker images by running the following in appropriate folders: 
      ```
      docker build -t mqtt_broker .
      ```
  2. Create docker network (suggestion `mqtt`): 
      ```
      docker network create --driver bridge <network_name>
      ```
   3. Start mqtt broker container on created network with port 1883 mapped:
      ```
      docker run -d --name mqtt_broker --network <network_name> -p 1883:1883 mqtt_broker
      ```
   4. Build file processor image with three key parameters: 
        a. `<AWS_ACCESS_KEY>` which is the aws access key for the account associated with the s3 bucket to save files to
        b. `<AWS_SECRET_ACCESS_KEY>` which is aws secret access key for the account associated with the s3 bucket to save files to
        c. `<S3_BUCKET_NAME>` which is the s3 bucket name
      ```
      sudo docker build --build-arg AWS_ACCESS_KEY=<AWS_ACCESS_KEY> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg S3_BUCKET_NAME=<S3_BUCKET_NAME> -t file_processor .
      ```
   5. Run file processor container
      ```
      docker run -d -it --name file_processor --privileged --network <network_name> file_processor bash
      ```
   6. Run script in file processor container to activate aws s3 file mapping
      ```
      docker exec file_processor /start-script.sh
      ```
   7. Run script in file processor container to start file processor
      ```
      docker exec file_processor python3 -u file_processor.py mqtt_broker topic &
      ```
