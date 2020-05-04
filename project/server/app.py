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

@app.route("/time", methods=["GET"])
def get_current_time():
    return jsonify({"time": time.time()})

@app.route("/job", methods=["POST"])
def create_task():
    message = request.json
    print(f"Message: {message}")
    
    uid = str(uuid.uuid4())
    print(f"UID: {uid}")
    if message: tasks.create_task(message, uid)
    return jsonify({"time": time.time()})

app.run()
