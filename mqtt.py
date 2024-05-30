# import serial.tools.list_ports
import sys
import time
import os
# from   import load_dotenv
import paho.mqtt.client as mqttClient


class MQTTClient:
    _instance = None

    recvCallBack = None

    def setRecvCallBack(self, func):
        self.recvCallBack = func

    def __new__(cls, mqtt_server, mqtt_port, topics, mqtt_username, mqtt_password):
        if cls._instance is None:
            cls._instance = super(MQTTClient, cls).__new__(cls)

            cls._instance.mqtt_server = mqtt_server
            cls._instance.mqtt_port = mqtt_port
            cls._instance.topics = topics
            cls._instance.mqtt_username = mqtt_username
            cls._instance.mqtt_password = mqtt_password

            cls._instance.client = mqttClient.Client(
                mqttClient.CallbackAPIVersion.VERSION1
            )
            cls._instance.client.on_connect = cls._instance.on_connect
            cls._instance.client.on_message = cls._instance.on_message
            cls._instance.client.on_subscribe = cls._instance.on_subscribe
            cls._instance.client.on_disconnect = cls._instance.on_disconnect

        return cls._instance

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            for f in self.topics:
                print("Subscribing to " + f)
                client.subscribe(f)
            print("Connected to broker")
        else:
            print(f"Connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        topicSub=""
        if(str(msg.topic)=="/innovation/airmonitoring/smarthome/detect_falling"):
            topicSub = "FALLING_DETECTION"
      
        print("Received " + payload + " from " + topicSub)
      
       
                

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed Successfully")

    def on_disconnect(self, client, userdata, rc, properties=None):
        print("Disconnected from broker")
        sys.exit(1)

    def publishMessage(self, topic, msg):
        self.client.publish(topic, msg)
        topicPub=""
        if(str(topic) =="/innovation/airmonitoring/smarthome/detect_falling"):
            topicPub = "FALLING_DETECTION"
       
        print("Published to " + topicPub + " with value: " + msg)

    def connect(self):
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.client.connect(self.mqtt_server, int(self.mqtt_port))
        self.client.loop_start()