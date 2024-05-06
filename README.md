# Image Privacy Protection

## Project Setup

This project consists of a Flask server and a React client using Vite & npm. Follow the instructions below to get started.

## Overview

This application uses a Python Flask backend server to perform object detection with YOLOv3 and blurring sensitive information using OpenCV. The system architecture includes a UI client that sends input images to the Flask backend. Object detection is performed on the backend, and the processed image with blurred objects is sent back to the UI client.

## Prerequisites

• Python 3.x

• pip (Python package installer)

• virtualenv (to create a virtual environment for Python projects)

## Setup
   
1. Change directory to the server folder.

      `cd server`
   

2. Install virtualenv using pip if it's not already installed.

      `pip install virtualenv`
   

3. Create a virtual environment in the server directory.

      `virtualenv flask_env`
   

4. Activate the virtual environment.

   For Windows:
      `flask_env\Scripts\activate`
   

   For MacOS/Linux:
      `source flask_env/bin/activate`
   

5. Install the required Python packages using pip.

      `pip install flask flask_cors requests Pillow torch torchvision opencv-python`
   

6. Run the Flask application.

      `python src/app.py`
   
