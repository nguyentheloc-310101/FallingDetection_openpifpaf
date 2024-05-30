# import serial.tools.list_ports
import sys
import time
import os
from simpleAI import *
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
        if(str(msg.topic)=="theloc3101/feeds/button-light"):
            topicSub = "BUTTON_LIGHT"
        elif(str(msg.topic)=="theloc3101/feeds/humid_history"):
            topicSub = "HUMID_HISTORY"
        elif(str(msg.topic)=="theloc3101/feeds/temperature_history"):
            topicSub = "TEMPERATURE_HISTORY"
        elif(str(msg.topic)=="theloc3101/feeds/light_history"):
            topicSub = "LIGHT_HISTORY"
        elif(str(msg.topic) =="theloc3101/feeds/button2"):
            topicSub = "BUMP_BUTTON_FEED"
        print("Received " + payload + " from " + topicSub)
        if (str(msg.topic) == "theloc3101/feeds/button-light"):
            if payload == "0":
                self.recvCallBack("button-light-off")
            else:
                self.recvCallBack("button-light-on")
        elif (str(msg.topic) == "theloc3101/feeds/button2"):
            if payload == "0":
                self.recvCallBack("button-bump-off")
            else:
                self.recvCallBack("button-bump-on")
       
                

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed Successfully")

    def on_disconnect(self, client, userdata, rc, properties=None):
        print("Disconnected from broker")
        sys.exit(1)

    def publishMessage(self, topic, msg):
        self.client.publish(topic, msg)
        topicPub=""
        if(str(topic) =="theloc3101/feeds/button-light"):
            topicPub = "BUTTON_LIGHT_FEED"
        elif(str(topic) =="theloc3101/feeds/humid_history"):
            topicPub = "HUMID_HISTORY_FEED"
        elif(str(topic) =="theloc3101/feeds/temperature_history"):
            topicPub = "TEMPERATURE_HISTORY_FEED"
        elif(str(topic) =="theloc3101/feeds/light_history"):
            topicPub = "LIGHT_HISTORY_FEED"
        elif(str(topic) =="theloc3101/feeds/button2"):
            topicPub = "BUMP_BUTTON_FEED"
        print("Published to " + topicPub + " with value: " + msg)

    def connect(self):
        self.client.username_pw_set(self.mqtt_username, self.mqtt_password)
        self.client.connect(self.mqtt_server, int(self.mqtt_port))
        self.client.loop_start()