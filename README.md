# Automatic Image Privacy Enhancement For Secure Sharing

## Overview

The objective of this project is to address the prevalent issue of privacy vulnerabilities associated with sharing images online. The project aims to develop a robust system capable of protecting individuals’ privacy while sharing images online. By implementing advanced algorithms and techniques, the system will effectively detect and blur out sensitive details, thus minimizing the potential for misuse of personal information. The application uses a Python Flask backend server to perform object detection with YOLOv3 and blurring sensitive information using OpenCV. The system architecture includes a UI client that sends input images to the Flask backend. Object detection is performed on the backend, and the processed image with blurred objects is sent back to the UI client.

## System Architecture

_Insert Image here_

## Setup

### Backend Server
   
Inside the server/ directory, create a virtual environment for the backend code

```
pip install virtualenv
python3 -m venv flask_env
cd flask_env
source Scripts/activate
``` 

Install the required Python packages using pip.

`pip install flask flask_cors requests Pillow torch torchvision opencv-python`

Copy the [YOLOv3](https://pjreddie.com/darknet/yolo/) object detection [weights file](https://pjreddie.com/media/files/yolov3.weights) to the src/ directory

6. Run the Flask application.

`python src/app.py`

The Flask application will be listening at the **http://localhost:5000**

### UI Client

After installinng Node.js, run the below steps inside the client/ directory to setup the UI client

```
npm install
npm run dev
```

The UI client will be available at **https://localhost:5173**

## Website Usage

- Drag and drop an image to the box or click on the “click to browse file” text to select an image from the system
- ⁠After selecting an image, click on the “Upload Image” button
- ⁠For preview dikhega below the button and on the left, and on the right, you will see Object detected in the image
- ⁠For you can select the particular objects you want to blur and select the blur level (1-5)
- ⁠Then click on “Protect my Image” button to apply the filters and blur the image (preview visible on the left)
- ⁠Finally, click on the “Download Image” button to download the output image

Below is an example of how the output image will look like once the sensitive information has been hidden -

_Insert Image here_
