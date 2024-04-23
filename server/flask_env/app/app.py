import io
import base64
from flask import Flask, request, jsonify
from PIL import Image, ImageDraw
import torchvision.transforms as transforms
import torch
import image_utils, text_utils
import re
import numpy as np
import cv2
from flask_cors import CORS
import image_utils

app = Flask(__name__)
CORS(app)


# Define transformation to preprocess the image
transform = transforms.Compose(
    [
        transforms.ToTensor(),
    ]
)



def blur_sensitive_info(file_path, blur_level=1):
    image = cv2.imread(file_path)
    contains_faces = image_utils.scan_image_for_people(image)

    original, intelligible = image_utils.scan_image_for_text(image)
    text = original
    rules=text_utils.get_regexes()
    addresses = text_utils.regional_pii(text)
    emails = text_utils.email_pii(text, rules)
    phone_numbers = text_utils.phone_pii(text, rules)

    keywords_scores = text_utils.keywords_classify_pii(rules, intelligible)
    score = max(keywords_scores.values())
    pii_class = list(keywords_scores.keys())[list(keywords_scores.values()).index(score)]

    country_of_origin = rules[pii_class]["region"]

    identifiers = text_utils.id_card_numbers_pii(text, rules)

    if score < 5:
        pii_class = None

    if len(identifiers) != 0:
        identifiers = identifiers[0]["result"]

    print("contains_faces: ", contains_faces)
    print("addresses: ", addresses)
    # Blur sensitive information in the image
    if contains_faces>0:
        image = image_utils.blur_faces(image)

    if addresses:
        image = image_utils.blur_regions(image, addresses)

    if emails:
        image = image_utils.blur_regions(image, emails)

    if phone_numbers:
        image = image_utils.blur_regions(image, phone_numbers)

    # if identifiers:
    #     image = image_utils.blur_regions(image, identifiers)

    # Convert the image back to PIL format
    blurred_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # blurred_img = Image.fromarray(image)

    return blurred_img
    
@app.route("/blur_sensitive_info", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    blur_level = int(request.form.get("blur_level", 1))

    image = request.files["image"]
    img = Image.open(image)

    temp_image_path = "./" + "temp_image.jpg"
    img.save(temp_image_path)
    # Blur sensitive information in the image with the specified blur level
    blurred_img = blur_sensitive_info(temp_image_path, blur_level)

    # Convert the blurred image to bytes and then to base64
    buffered = io.BytesIO()
    blurred_img.save(buffered, format="JPEG")
    blurred_img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"blurred_image": blurred_img_str}), 200


if __name__ == "__main__":
    app.run(debug=True)
