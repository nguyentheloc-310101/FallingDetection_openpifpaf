import cv2
import cvzone
from mqtt import MQTTClient
import math
import os
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))  # Ensure the port is an integer
print(MQTT_PORT)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPICS = ["/innovation/airmonitoring/smarthome/detect_falling"]

def test(payload):
    print("data: " + payload)

mqttClient = MQTTClient(MQTT_SERVER, MQTT_PORT, TOPICS, MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.setRecvCallBack(test)
mqttClient.connect()


print('Fall detection')
mqttClient.publishMessage("/innovation/airmonitoring/smarthome/detect_falling", '{"falling":1}');