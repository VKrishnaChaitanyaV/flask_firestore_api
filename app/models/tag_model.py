from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Tag(BaseModel):
    tagid: Optional[str]
    name: str = Field(..., description="Tag name must be provided")
    usage_count: Optional[int] = 1
    createdAt: datetime
    last_used: Optional[datetime]