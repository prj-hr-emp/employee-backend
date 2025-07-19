from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    class Config:
        orm_mode = True

class LeaveRequestCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str

class LeaveRequestOut(LeaveRequestCreate):
    id: int
    status: str
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

class SalarySlipOut(BaseModel):
    id: int
    month: str
    download_url: str
    class Config:
        orm_mode = True

class BadgeOut(BaseModel):
    id: int
    name: str
    date_awarded: str
    class Config:
        orm_mode = True

class PulseBreakdown(BaseModel):
    punctuality: int
    attendance: int
    feedback: int
    overall: float

class OnboardingProgress(BaseModel):
    completed_steps: List[str]
    total_steps: int

class TeamRank(BaseModel):
    team: str
    rank: int
    total_teams: int
