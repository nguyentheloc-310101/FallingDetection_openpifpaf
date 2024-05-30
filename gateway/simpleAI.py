
from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
labels = open("labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)


def imageDetector():
    try:
        # Grab the webcamera's image.
        ret, image = camera.read()

        if image is None:
            raise Exception("Cannot read from camera")

        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

        # Show the image in a window
        # cv2.imshow("Webcam Image", image)

        # Make the image a numpy array and reshape it to the models input shape.
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

        # Normalize the image array
        image = (image / 127.5) - 1

        # Predicts the model
        prediction = model.predict(image)
        index = np.argmax(prediction)
        result = labels[index]
        confidence_score = prediction[0][index]

        # Print prediction and confidence score
        print("Class:", result[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

        return result[2:], confidence_score
    except Exception as e:
        print(e)
        return None, None


# camera.release()
# cv2.destroyAllWindows()
