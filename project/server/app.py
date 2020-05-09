# project/server/app.py

# == Import(s) ==
# => Local
from . import tasks

# => System
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

    jobId = str(uuid.uuid4())
    return jsonify({ "jobId": jobId })

@app.route("/api/job", methods=["POST"])
def create_job():
    message = request.json
    receipt:str = message.get("receipt"); package:list = message.get("package")
    if package:
        job = list(map(
            lambda raw: {
                "env": raw['env'],
                "name": raw['name'],
                "lut": {
                    "usrId": raw['usrId']
                }
            }, package))

        jobId = str(uuid.uuid4())
        if job: tasks.create_job(job, receipt, jobId)
        return jsonify({ "jobId": jobId })
    return "Invalid 'package' Data", 400

app.run()
