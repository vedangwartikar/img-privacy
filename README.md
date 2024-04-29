# Image Privacy Protection

## Project Setup

This project consists of a Flask server and a React client using Vite & pnpm. Follow the instructions below to get started.

## Server Setup

The server is a Flask application. To start the server, navigate to the server directory and activate the virtual environment named "flask_env". If you haven't created the virtual environment yet, you can do so using the following commands:

```bash
cd server
virtualenv flask_env
```

Activate the virtual environment:

```bash
source flask_env/bin/activate
```

Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

Then, start the Flask server.

```bash
export FLASK_APP=app.py
flask run
```

The server will start on http://localhost:5000.

## Client Setup

The client is a React application built using Vite and `pnpm`. To start the client, navigate to the client directory and install the required dependencies.

```bash
cd client
pnpm install
```

Then, start the Vite server.

```bash
pnpm run dev
```

The client will start on http://localhost:5173.

Now, you can open your browser and navigate to http://localhost:5173 to see the application. The client will communicate with the server on http://localhost:5000.

Remember to start the server before the client, as the client depends on the server for API calls.
