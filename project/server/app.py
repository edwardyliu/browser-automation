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
# => Flask
app = Flask("__main__")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# == HTTP Request(s) ==
@app.route("/api/keys", methods=["GET"])
def get_keys():
    return jsonify(tasks.get_keys())

@app.route("/api/scan", methods=["POST"])
def create_scan():
    scanId = str(uuid.uuid4())
    tasks.create_scan(request.json, scanId)
    
    return jsonify({ "scanId": scanId })

@app.route("/api/job", methods=["POST"])
def create_job():
    jobId = str(uuid.uuid4())
    tasks.create_job(request.json, jobId)

    return jsonify({ "jobId": jobId })

app.run()
