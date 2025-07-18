from app.repository import jobs_repository
from app.services import tag_service, user_service
from app.models.job_model import Job
from datetime import datetime
from typing import List

def create_job(job_data):
    now_iso = datetime.utcnow().isoformat()
    job_data['createdAt'] = now_iso
    job_data['updatedAt'] = now_iso

    # Handle tags
    tags_input = job_data.get('tags', [])
    tag_ids: List[str] = []
    tag_names: List[str] = []

    if tags_input:
        tag_infos = tag_service.upsert_tags_batch(tags_input)
        tag_ids = [tag.tagid for tag in tag_infos]
        tag_names = [tag.name for tag in tag_infos]

    job_data['tag_ids'] = tag_ids
    job_data['tag_names'] = tag_names
    job_data.pop('tags', None)  # Remove raw 'tags' field

    job = Job(**job_data)
    return jobs_repository.create_job(job.dict())

def create_jobs_batch(jobs_list):
    now_iso = datetime.utcnow().isoformat()
    validated_jobs = []

    for job_data in jobs_list:
        job_data['createdAt'] = now_iso
        job_data['updatedAt'] = now_iso

        # Handle tags per job
        tags_input = job_data.get('tags', [])
        tag_ids: List[str] = []
        tag_names: List[str] = []

        if tags_input:
            tag_infos = tag_service.upsert_tags_batch(tags_input)
            tag_ids = [tag.tagid for tag in tag_infos]
            tag_names = [tag.name for tag in tag_infos]

        job_data['tag_ids'] = tag_ids
        job_data['tag_names'] = tag_names
        job_data.pop('tags', None)

        job = Job(**job_data)
        validated_jobs.append(job.dict())

    return jobs_repository.create_jobs_batch(validated_jobs)

def get_job(jobid):
    doc = jobs_repository.get_job_by_id(jobid)
    return doc.to_dict() if doc else None

def update_job(jobid, job_data):
    job_data['updatedAt'] = datetime.utcnow().isoformat()
    existing = get_job(jobid)
    if not existing:
        return None

    # Handle tags if updated
    tags_input = job_data.get('tags', [])
    if tags_input:
        tag_infos = tag_service.upsert_tags_batch(tags_input)
        job_data['tag_ids'] = [tag.tagid for tag in tag_infos]
        job_data['tag_names'] = [tag.name for tag in tag_infos]
        job_data.pop('tags', None)

    updated_data = {**existing, **job_data}
    job = Job(**updated_data)  # validate
    return jobs_repository.update_job(jobid, job_data)

def delete_job(jobid):
    return jobs_repository.delete_job(jobid)

# def list_all_jobs():
#     jobs = jobs_repository.list_jobs()

#     return 

from typing import List, Optional

def list_all_jobs() -> List[dict]:
    # Step 1: Retrieve all jobs from jobs repository
    jobs = jobs_repository.list_jobs()  # Assuming this returns a list of jobs (list of dicts or objects)
    
    # Step 2: Extract user IDs from jobs and get user details for each user
    user = {}
    
    for job in jobs:
        user_id = job.get('userid')  # Assuming each job has a 'user_id' field
        if user_id:
            job["user"] = user_service.get_user(user_id)
    
    # Step 3: Return the list of user details
    return jobs

def get_user(userid: str) -> Optional[dict]:
    # Step 1: Retrieve user details by user ID from user repository
    doc = user_service.get_user(userid)
    
    # Step 2: Return user details if the document exists, otherwise None
    return doc.to_dict() if doc.exists else None

