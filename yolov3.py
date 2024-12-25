import os
import cv2
import numpy as np
import pyttsx3
import threading
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Predefined responses
RESPONSES = [
    "The street is cobbled with black railings to the left presumably separating the road for the cars from the pedestrian walkways. In the middle of the street is a streetcar whose bottom half is yellow and is covered in graffiti. The street is flanked on both sides by colorful buildings.",
    "There is a big tractor (or whatever it's called) in the middle of the road that looks like it's equipment used for farming. There is a giant mass of hay behind the tractor. The tractor itself is the color of reddish orange and has front wheels that are substantially smaller than the back wheels. On top of the tractor, there is a man wearing dark clothes and a red hat who is waving to the camera.",
    "There are two men wearing white shirts in the photo. Both are wearing black graduation caps. One who is wearing tight pants is pushing a trolley with black plastic-looking boxes that are stacked within another, and the other is carrying these boxes in his arms."
]

# Load YOLO model
def load_yolo():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return net, classes, output_layers

# Detect objects in the image
def detect_objects(image, net, classes, output_layers):
    img = np.array(image)
    height, width, _ = img.shape

    # Create blob and run YOLO detection
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    # Parse YOLO output
    detected_labels = []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Confidence threshold
                detected_labels.append(classes[class_id])

    return detected_labels

# Match detected labels to predefined responses
def match_response(detected_labels):
    if "train" in detected_labels or "streetcar" in detected_labels:
        return RESPONSES[0]
    elif "tractor" in detected_labels or "person" in detected_labels and "hat" in detected_labels:
        return RESPONSES[1]
    elif "person" in detected_labels and "graduation cap" in detected_labels:
        return RESPONSES[2]
    else:
        return "No matching response found for the detected image."

# Speak the response in a separate thread
def speak_response(response):
    def speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(response)
        engine.runAndWait()

    thread = threading.Thread(target=speak)
    thread.start()

# Serve the HTML file
@app.route('/')
def home():
    return render_template('yolo.html')

# Serve the manifest.json file
@app.route('/manifest.json')
def manifest():
    return send_from_directory('.', 'manifest.json')

# Process the image and generate a response
@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        image_data = data['image']

        # Decode the Base64 image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(BytesIO(image_data)).convert("RGB")

        # Load YOLO model
        net, classes, output_layers = load_yolo()

        # Detect objects
        detected_labels = detect_objects(image, net, classes, output_layers)

        # Match response
        matched_response = match_response(detected_labels)

        # Speak the response
        speak_response(matched_response)

        return jsonify({"response": matched_response})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

# Serve static files for CSS or JS if needed
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
