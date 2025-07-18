from app import db
from app.config import Config
from datetime import datetime

collection = db.collection(Config.JOBS_COLLECTION)

def create_job(data: dict) -> dict:
    doc_ref = collection.document()
    data['jobid'] = doc_ref.id
    data['createdAt'] = datetime.utcnow()
    doc_ref.set(data)
    return data

def create_jobs_batch(jobs_data: list[dict]) -> list[dict]:
    batch = db.batch()
    created_jobs = []

    for job_data in jobs_data:
        doc_ref = collection.document()
        job_data['jobid'] = doc_ref.id
        batch.set(doc_ref, job_data)
        created_jobs.append(job_data)

    batch.commit()
    return created_jobs

def get_job_by_id(jobid: str):
    doc = collection.document(jobid).get()
    if doc.exists:
        return doc.to_dict()
    return None

def update_job(jobid: str, data: dict):
    data.pop("jobid", None)  # Prevent jobid overwrite
    data["updatedAt"] = datetime.utcnow()
    return collection.document(jobid).update(data)

def activate_job(jobid: str):
    return collection.document(jobid).update({
        "active": True,
        "updatedAt": datetime.utcnow()
    })

def delete_job(jobid: str):
    return collection.document(jobid).update({
        "active": False,
        "updatedAt": datetime.utcnow()
    })

def list_jobs():
    return [doc.to_dict() for doc in collection.stream()]
