FROM alpine:latest
RUN apk add mosquitto
# Configure to allow remote access
RUN echo "allow_anonymous true" > /etc/mosquitto/mosquitto.conf
RUN echo "listener 1883 0.0.0.0" >> /etc/mosquitto/mosquitto.conf
CMD ["mosquitto","-c","/etc/mosquitto/mosquitto.conf"]
