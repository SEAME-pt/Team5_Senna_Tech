# Taxi_Robot_Server

This document explains how to set up and run the Taxi Robot server locally.

## 1. Prerequisites

Make sure you have Python 3 installed on your machine.

Check the version:

```bash
python3 --version
```

## 2. Create and activate a virtual environment

From the repository root, go to the server folder:

```bash
cd ADAS/Taxi_Robot_Server
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

If you are using a different shell, the activation command may vary, but the virtual environment will be created in the `.venv` folder inside this directory.

## 3. Install the Python dependencies

With the virtual environment activated, install the required packages:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Run the server

Start the FastAPI application with Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You can also use:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 5. Verify that the server is running

Open the following URL in your browser or with curl:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status": "ok"}
```

## 6. Useful endpoints

- Health check: `GET /health`
- Mission command: `POST /mission/command`
- Status: `GET /status`
- WebSocket endpoint: `WS /ws/robotaxi`

## 7. Stop the server

Press `Ctrl + C` in the terminal where the server is running.
