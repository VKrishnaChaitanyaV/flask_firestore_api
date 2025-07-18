import os

class Config:
    PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "your-project-id")
    USER_COLLECTION = "users"
    JOBS_COLLECTION = "jobs"
    TAGS_COLLECTION = "tags"