# project/server/views/api.py

# === Import(s) ===
# => Local <=
from project.server.tasks import keys
from project.server.tasks import create_job
from project.server.tasks import create_scan

# => System <=
import uuid

# => External <=
import redis
from rq import Queue, Connection
from flask import Blueprint, jsonify, request, current_app

# === Flask Blueprint ===
api = Blueprint("api", __name__)

# => Route(s) <=
@api.route("/keys", methods=["GET"])
def get_keys():
    return jsonify(keys)

@api.route("/job", methods=["POST"])
def run_job():
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        job_id = str(uuid.uuid4())
        q = Queue()
        task = q.enqueue(create_job, args=(request.json, job_id,), job_id=job_id)

    return jsonify({ "jobId": task.get_id() })

@api.route("/scan", methods=["POST"])
def run_scan():
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        scan_id = str(uuid.uuid4())
        q = Queue()
        task = q.enqueue(create_scan, args=(request.json, scan_id,), job_id=scan_id)
    
    return jsonify({ "scanId": task.get_id() })
