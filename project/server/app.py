# project/server/app.py

# == Import(s) ==
# => Local
from . import tasks

# => System
import time
import uuid

# => External
from flask import Flask, request, jsonify
from flask_cors import CORS

# == Application ==
app = Flask("__main__")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks.get_task_keys())

@app.route("/api/scan", methods=["POST"])
def create_scan():
    message = request.json
    print(f"Message: {message}")

    uid = str(uuid.uuid4())
    return jsonify({ "jobId": uid })

@app.route("/api/job", methods=["POST"])
def create_job():
    message = request.json
    print(f"Message: {message}")
    
    uid = str(uuid.uuid4())
    if message: tasks.create_job(message, uid)
    return jsonify({ "jobId": uid })

app.run()
