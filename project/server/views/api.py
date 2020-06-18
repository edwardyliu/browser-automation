# project/server/views/api.py

# === Import(s) ===
# => Local <=
from .. import tasks

# => System <=
import uuid

# => External <=
import redis
from rq import Queue, Connection
from flask import Blueprint, jsonify, request, current_app

# === Flask Blueprint ===
api = Blueprint("api", __name__)

# => Route(s) <=
# Method: Get(s)
@api.route("/keys", methods=["GET"])
def get_keys():
    return jsonify(tasks.keys())

@api.route("/job/<job_id>", methods=["GET"])
def get_status(job_id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue()
        job = q.fetch_job(job_id)
    
    if job:
        response = {
            "status": "success",
            "data": {
                "job_id": job.get_id(),
                "job_status": job.get_status(),
                "job_result": job.result,
            },
        }
    else:
        response = { "status": "error" }
    return jsonify(response)

# Method: Post(s)
@api.route("/job", methods=["POST"])
def run_job():
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        job_id = str(uuid.uuid4())
        q = Queue()
        job = q.enqueue(tasks.create_job, args=(request.json, job_id, current_app.config["WEBDRIVER"],), job_id=job_id)

    response = {
        "status": "success",
        "data": {
            "job_id": job.get_id(),
        },
    }

    return jsonify(response), 202

@api.route("/scan", methods=["POST"])
def run_scan():
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        job_id = str(uuid.uuid4())
        q = Queue()
        job = q.enqueue(tasks.create_scan, args=(request.json, job_id, current_app.config["WEBDRIVER"],), job_id=job_id)
    
    response = {
        "status": "success",
        "data": {
            "job_id": job.get_id(),
        },
    }

    return jsonify(response), 202
