# project/server/app.py

# == Import(s) ==
# => Local
from . import tasks

# => System
import time

# => External
from flask import Flask, request, jsonify

# == Application ==
app = Flask("__main__")

@app.route("/time", methods=["GET"])
def get_current_time():
    return jsonify({"time": time.time()})

@app.route("/job", methods=["POST"])
def exec_job():
    message = request.json
    parcel = message.get("parcel"); requestor = message.get("requestor")
    print(f"Message: {message}")

    if parcel: tasks.exec_job(parcel, requestor)
    return jsonify({"time": time.time()})

app.run()
