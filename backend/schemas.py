from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Application(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    business: str = Field(..., min_length=2, max_length=120)
    industry: str = Field(..., min_length=2, max_length=120)
    bottleneck: str = Field(..., min_length=5, max_length=2000)
    hours: str = Field(..., min_length=1, max_length=50)
    openToSystems: str = Field(..., pattern=r"^(Yes|No)$")
    timeframe: str = Field(..., min_length=3, max_length=50)

class ApplicationOut(Application):
    id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
