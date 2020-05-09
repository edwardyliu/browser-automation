# project/server/app.py

# == Import(s) ==
# => Local
from . import tasks

# => System
import time
import uuid

# => External
from flask import Flask, request, jsonify

# == Application ==
app = Flask("__main__")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks.get_task_keys())

@app.route("/scan", methods=["POST"])
def create_scan():
    message = request.json
    print(f"Message: {message}")

    return jsonify({"time": time.time()})

@app.route("/job", methods=["POST"])
def create_job():
    message = request.json
    print(f"Message: {message}")
    
    uid = str(uuid.uuid4())
    if message: tasks.create_job(message, uid)
    return jsonify({"time": time.time()})

app.run()
