from flask import Blueprint, request, jsonify
from app.services import job_service
from pydantic import ValidationError

job_bp = Blueprint("job_bp", __name__)

@job_bp.route("/", methods=["POST"])
def create_job():
    try:
        data = request.json
        job_service.create_job(data)
        return jsonify({"message": "Job created"}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@job_bp.route("/batch", methods=["POST"])
def create_jobs_batch():
    try:
        jobs_list = request.json
        created_jobs = job_service.create_jobs_batch(jobs_list)
        return jsonify({"message": "Jobs created", "jobs": created_jobs}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@job_bp.route("/<jobid>", methods=["GET"])
def get_job(jobid):
    job = job_service.get_job(jobid)
    if job:
        return jsonify(job)
    return jsonify({"error": "Job not found"}), 404

@job_bp.route("/<jobid>", methods=["PUT"])
def update_job(jobid):
    data = request.json
    result = job_service.update_job(jobid, data)
    if result is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"message": "Job updated"})

@job_bp.route("/inactivate/<jobid>", methods=["PUT"])
def delete_job(jobid):
    result = job_service.activate_job(jobid)
    if result is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"message": "Job Inactivated"})

@job_bp.route("/activate/<jobid>", methods=["PUT"])
def activate_job(jobid):
    result = job_service.delete_job(jobid)
    if result is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"message": "Job Activated"})

@job_bp.route("/", methods=["GET"])
def list_jobs():
    jobs = job_service.list_all_jobs()
    return jsonify(jobs)
