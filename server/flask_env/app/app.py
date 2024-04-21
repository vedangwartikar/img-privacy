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

app = Flask(__name__)
CORS(app)

# Load the Faster R-CNN ResNet50 model
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Define transformation to preprocess the image
transform = transforms.Compose(
    [
        transforms.ToTensor(),
    ]
)


def blur_sensitive_info(image, blur_level=1):
    # Preprocess the image
    image_tensor = transform(image).unsqueeze(0)

    # Run the model inference
    with torch.no_grad():
        output = model(image_tensor)

    # Get the predicted bounding boxes and labels
    boxes = output[0]["boxes"]

    # Convert PIL image to OpenCV format
    cv_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Apply Gaussian blur to sensitive regions (e.g., faces) with different intensity based on blur level
    for box in boxes:
        box = box.cpu().numpy().astype(int)
        x1, y1, x2, y2 = box
        face = cv_img[y1:y2, x1:x2]
        blur_intensity = (
            5 * blur_level
        )  # Adjust the blur intensity based on the specified level
        blurred_face = cv2.GaussianBlur(
            face, (23, 23), blur_intensity
        )  # Adjust parameters as needed
        cv_img[y1:y2, x1:x2] = blurred_face

    # Convert back to PIL image
    blurred_image = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    return blurred_image


@app.route("/blur_sensitive_info", methods=["POST"])
def process_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    blur_level = int(request.form.get("blur_level", 1))

    image = request.files["image"]
    img = Image.open(image)

    # Blur sensitive information in the image with the specified blur level
    blurred_img = blur_sensitive_info(img, blur_level)

    # Convert the blurred image to bytes and then to base64
    buffered = io.BytesIO()
    blurred_img.save(buffered, format="JPEG")
    blurred_img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"blurred_image": blurred_img_str}), 200


if __name__ == "__main__":
    app.run(debug=True)
