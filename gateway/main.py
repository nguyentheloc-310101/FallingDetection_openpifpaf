import time
from mqtt import MQTTClient
import os
from dotenv import load_dotenv
from simpleAI import *
from uart import *
load_dotenv()
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = os.getenv("MQTT_PORT")
print(MQTT_PORT)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPICS = ["theloc3101/feeds/button-light","theloc3101/feeds/humid_history","theloc3101/feeds/light_history","theloc3101/feeds/temperature_history","theloc3101/feeds/button2"]


def test(payload):
    print("data: " + payload)


mqttClient = MQTTClient(MQTT_SERVER, MQTT_PORT, TOPICS, MQTT_USERNAME, MQTT_PASSWORD)
# mqttClient.setRecvCallBack(test)
mqttClient.setRecvCallBack(writeSerial)
mqttClient.connect()

counter_ai = 5

while True:
    # value = input('input value : ')
    # if(value=="L1"):
    #     mqttClient.publishMessage("theloc3101/feeds/button-light", "1")
    # elif(value=="L0"):
    #     mqttClient.publishMessage("theloc3101/feeds/button-light", "0")
    # if(value=="B1"):
    #     mqttClient.publishMessage("theloc3101/feeds/button2", "1")
    # elif(value=="B0"):
    #     mqttClient.publishMessage("theloc3101/feeds/button2", "0")
    # else:
    #     print('Invalid syntax')
    
    # counter_ai -= 1
    # if counter_ai <= 0:
    #     result, confidence_score = imageDetector()
    #     if result is not None and confidence_score is not None:
    #         msg = result + " " + str(np.round(confidence_score * 100))[:-2]
    #         mqttClient.publishMessage("theloc3101/feeds/ai-camera", msg)
    #     counter_ai = 5
    readSerial(mqttClient)
    # time.sleep(1)

