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

# Set up the RTSP stream capture with a public RTSP link
rtsp_link = 'http://172.20.10.2:81/stream'
cap = cv2.VideoCapture(rtsp_link)

# Check if the capture is opened correctly
if not cap.isOpened():
    print("Error: Could not open RTSP stream.")
    exit()

# Set resolution to 4:3 aspect ratio (e.g., 640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set FFmpeg parameters for better handling
cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)  # Buffer size to hold frames
cap.set(cv2.CAP_PROP_FPS, 30)  # Set FPS if known

model = YOLO('yolov8s.pt')

# Load class names
classnames = []
with open('classes.txt', 'r') as f:
    classnames = f.read().splitlines()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    results = model(frame)

    for info in results:
        parameters = info.boxes
        for box in parameters:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            confidence = box.conf[0]
            class_detect = box.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            conf = math.ceil(confidence * 100)

            # Implement fall detection using the coordinates x1, y1, x2, y2
            height = y2 - y1
            width = x2 - x1
            threshold = height - width

            if conf > 80 and class_detect == 'person':
                cvzone.cornerRect(frame, [x1, y1, width, height], l=30, rt=6)
                cvzone.putTextRect(frame, f'{class_detect}', [x1 + 8, y1 - 12], thickness=2, scale=2)

            if threshold < 0:
                print('Fall detection')
                mqttClient.publishMessage("/innovation/airmonitoring/smarthome/detect_falling", '{"falling":1}')
                cvzone.putTextRect(frame, 'Fall Detected', [height, width], thickness=2, scale=2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

cap.release()
cv2.destroyAllWindows()
