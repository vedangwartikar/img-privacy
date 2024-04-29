import io
import base64
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw
import torchvision.transforms as transforms
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
import numpy as np
import cv2
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

labels_url = "https://raw.githubusercontent.com/amikelive/coco-labels/master/coco-labels-2014_2017.txt"

LABELS = requests.get(labels_url).text.strip().split("\n")


def detect_objects(image, selected_labels_original):
    selected_labels = selected_labels_original.copy()

    if "face" in selected_labels:
        if "person" in selected_labels:
            selected_labels.remove("face")
        else:
            selected_labels.append("person")

    # Load MSCOCO labels and pre-trained model
    net = cv2.dnn.readNet("./src/yolov3.weights", "./src/yolov3.cfg")
    # with open("./src/coco.names", "w") as f:
    #     f.write("\n".join(LABELS))

    # Load image and convert to blob
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)

    # Set input and perform forward pass
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)

    # Process detections
    boxes = []
    confidences = []
    class_ids = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * image.shape[1])
                center_y = int(detection[1] * image.shape[0])
                w = int(detection[2] * image.shape[1])
                h = int(detection[3] * image.shape[0])
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    if len(selected_labels) == 0 or selected_labels[0] == "":
        return boxes, confidences, class_ids
    else:
        filtered_boxes = [
            box
            for box, class_id in zip(boxes, class_ids)
            if LABELS[class_id] in selected_labels
        ]
        filtered_class_ids = [
            class_id for class_id in class_ids if LABELS[class_id] in selected_labels
        ]

        return filtered_boxes, confidences, filtered_class_ids


def blur_objects(
    image,
    boxes,
    class_ids,
    selected_labels_original,
    blur_license_plate=False,
    blur_level=1,
):

    selected_labels = selected_labels_original.copy()

    if "face" in selected_labels:
        if "person" in selected_labels:
            selected_labels.remove("face")
        else:
            selected_labels.append("person")

    print("Selected labels:", selected_labels)

    # if "PII" in selected_labels:
    #     selected_labels.add("laptop", "tv", "cell phone")

    for i, box in enumerate(boxes):
        x, y, w, h = box

        class_id = class_ids[i]
        label = LABELS[class_id]

        if (
            label == "car" or label == "truck" or label == "bus"
        ) and "license plate" in selected_labels:
            # print("Car/Truck/Bus detected")

            license_plate_region = [
                int(x + w * 0.2),
                int(y + h * 0.5),
                int(w * 0.7),
                int(h * 0.1),
            ]

            roi = image[
                license_plate_region[1] : license_plate_region[1]
                + license_plate_region[3],
                license_plate_region[0] : license_plate_region[0]
                + license_plate_region[2],
            ]

            if roi.size == 0:
                continue

            blur_intensity = 1 + 0.5 * blur_level
            blurred_roi = cv2.GaussianBlur(roi, (25, 25), blur_intensity)

            image[
                license_plate_region[1] : license_plate_region[1]
                + license_plate_region[3],
                license_plate_region[0] : license_plate_region[0]
                + license_plate_region[2],
            ] = blurred_roi

        elif label == "person" and "face" in selected_labels:
            # print("Person detected")

            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )

            # Blur faces within the bounding box of the person
            for fx, fy, fw, fh in faces:
                face_roi = image[fy : fy + fh, fx : fx + fw]

                if face_roi.size == 0:
                    continue

                blur_intensity = 1 + 0.5 * blur_level
                blurred_face = cv2.GaussianBlur(face_roi, (25, 25), blur_intensity)

                image[fy : fy + fh, fx : fx + fw] = blurred_face

        elif (
            label == "laptop" or label == "tv" or label == "cell phone"
        ) and "device screens" in selected_labels:
            print("Laptop/TV/CellPhone detected")

        else:
            roi = image[y : y + h, x : x + w]

            if roi.size == 0:
                continue

            blur_intensity = 1 + 0.5 * blur_level
            blurred_roi = cv2.GaussianBlur(roi, (25, 25), blur_intensity)

            image[y : y + h, x : x + w] = blurred_roi

    return image


def blur_license_plate_func(
    image,
    boxes,
    class_ids,
    selected_labels_original=[],
    blur_license_plate=False,
    blur_level=1,
):

    selected_labels = selected_labels_original.copy()

    selected_labels.append("car")
    selected_labels.append("truck")
    selected_labels.append("bus")

    for i, box in enumerate(boxes):
        x, y, w, h = box

        class_id = class_ids[i]
        label = LABELS[class_id]

        if label == "car" or label == "truck" or label == "bus":
            # print("Car/Truck/Bus detected")

            license_plate_region = [
                int(x + w * 0.2),
                int(y + h * 0.4),
                int(w * 0.5),
                int(h * 0.7),
            ]

            roi = image[
                license_plate_region[1] : license_plate_region[1]
                + license_plate_region[3],
                license_plate_region[0] : license_plate_region[0]
                + license_plate_region[2],
            ]

            if roi.size == 0:
                continue

            blur_intensity = 1 + 0.5 * blur_level
            blurred_roi = cv2.GaussianBlur(roi, (25, 25), blur_intensity)

            image[
                license_plate_region[1] : license_plate_region[1]
                + license_plate_region[3],
                license_plate_region[0] : license_plate_region[0]
                + license_plate_region[2],
            ] = blurred_roi

    return image


@app.route("/blur_sensitive_info", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    blur_level = int(request.form.get("blur_level", 1))
    blur_license_plate = bool(int(request.form.get("blur_license_plate", 0)))
    selected_labels = request.form.get("labels", []).split(",")

    print("blur_license_plate:", blur_license_plate)  # True or False
    print("Selected labels:", selected_labels)  # car, person, etc.

    image = request.files["image"]
    img = Image.open(image)

    # Blur sensitive information in the image with the specified blur level

    # blurred_img = blur_sensitive_info(img, blur_level)

    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    boxes, _, class_ids = detect_objects(img, selected_labels)

    print("class_ids", class_ids)

    unique_labels = set()

    if len(selected_labels) == 0 or selected_labels[0] == "":
        for i, box in enumerate(boxes):
            label = LABELS[class_ids[i]]
            unique_labels.add(label)
            # print(label)

        print("Unique labels of the detected objects:", list(unique_labels))

        # if any(label in unique_labels for label in ["car", "truck", "bus"]):
        #     unique_labels.add("license plate")

        if any(label in unique_labels for label in ["person"]):
            unique_labels.add("face")

        if any(label in unique_labels for label in ["laptop", "tv", "cell phone"]):
            unique_labels.add("device screens")

        unique_labels.discard("laptop")
        unique_labels.discard("tv")
        unique_labels.discard("cell phone")

        print("Updated labels:", list(unique_labels))

    blurred_img = img

    if blur_license_plate:
        boxes_2, _, class_ids_2 = detect_objects(img, [])

        blurred_img = blur_license_plate_func(
            img, boxes_2, class_ids_2, selected_labels, blur_license_plate, blur_level
        )

    if "device screens" in selected_labels:
        # selected_labels_copy = selected_labels.copy()
        selected_labels_copy = []
        selected_labels_copy.append("laptop")
        selected_labels_copy.append("tv")
        selected_labels_copy.append("cell phone")

        boxes_2, _, class_ids_2 = detect_objects(blurred_img, selected_labels_copy)

        blurred_img = blur_objects(
            img,
            boxes_2,
            class_ids_2,
            selected_labels_copy,
            blur_license_plate,
            blur_level,
        )

    if len(selected_labels) != 0 and selected_labels[0] != "":

        blurred_img = blur_objects(
            blurred_img,
            boxes,
            class_ids,
            selected_labels,
            blur_license_plate,
            blur_level,
        )

    # cv2.imwrite("blurred_img.png", blurred_img)
    blurred_img = Image.fromarray(cv2.cvtColor(blurred_img, cv2.COLOR_BGR2RGB))

    # Convert the blurred image to bytes and then to base64
    buffered = io.BytesIO()
    blurred_img.save(buffered, format="JPEG")
    blurred_img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return (
        jsonify(
            {"blurred_image": blurred_img_str, "unique_labels": list(unique_labels)}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
