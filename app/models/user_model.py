from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    userid: str
    phone: str = Field(..., description="Phone number must be 10 digits")
    name: str = Field(..., description="Please enter name")
    company: Optional[str]
    designation: Optional[str]
    location: Optional[str]
    email: Optional[str]
    gender: Optional[str]
    change: Optional[bool]
    active: bool
    createdAt: datetime
    updatedAt: datetime
    resumeUrl: Optional[str]
    profileImage: Optional[str]
    role: Optional[str]
    experience: Optional[float]
    skills: List[str]
    linkedinUrl: Optional[str]
    githubUrl: Optional[str]
    bio: Optional[str]

    @validator("name")
    def validate_name(cls, v):
        if len(v) == 0:
            raise ValueError("Please enter name")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(v) != 10:
            raise ValueError("Phone number must be 10 digits")
        return v

    @validator("email")
    def validate_custom_email(cls, v):
        email_str = str(v)

        if (email_str.count('@') != 1 or
            email_str.count('.com') != 1 or
            not email_str.endswith('.com') or
            email_str.startswith('@') or
            '@' not in email_str or
            email_str.index('@') == 0):
            raise ValueError("Invalid email format")

        return v