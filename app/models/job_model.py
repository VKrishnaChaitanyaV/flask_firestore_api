from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.user_model import User

class Job(BaseModel):
    jobid: Optional[str]
    userid: str
    company: str
    designation: str
    experience: Optional[float]
    skills: List[str]
    openings: Optional[int]
    email: EmailStr
    workmode: Optional[str]
    additionalDetails: Optional[str]
    source: Optional[str]
    active: bool = True
    location: Optional[str]
    salaryRange: Optional[str]
    jobType: Optional[str]
    postedAt: Optional[datetime]
    expiryDate: Optional[datetime]
    tag_ids: Optional[List[str]] = []
    tag_names: Optional[List[str]] = []
    likes: int = 0
    dislikes: int = 0
    shares: int = 0
    report: int = 0
    createdAt: datetime
    updatedAt: Optional[datetime]
    commentsCount: int = 0
    user: User

    @validator("designation")
    def required_text_fields(cls, v):
        if not v or not v.strip():
            raise ValueError("Designation is required")
        return v
    
    @validator("company")
    def validate_company(cls, v):
        if not v or not v.strip():
            raise ValueError("Company is required")
        return v

    @validator("skills")
    def validate_skills(cls, v):
        if not v or len(v) == 0:
            raise ValueError("At least one skill is required")
        return v
