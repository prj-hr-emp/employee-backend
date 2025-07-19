from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.db.database import get_db
from app.models import models
from app.schemas import schemas
from app.core.security import get_password_hash, verify_password, create_access_token, decode_token
from app.core.enums import RoleEnum, LeaveStatusEnum
from datetime import datetime
from typing import List

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = decode_token(token)
    if not email:
        raise HTTPException(401, "Invalid auth")
    usr = db.query(models.User).filter(models.User.email == email).first()
    if not usr:
        raise HTTPException(401, "User not found")
    return usr

@router.post("/register", response_model=schemas.UserOut)
def register(u: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == u.email).first():
        raise HTTPException(400, "Email exists")
    hashed = get_password_hash(u.password)
    new = models.User(email=u.email, name=u.name, hashed_password=hashed, role=RoleEnum.employee)
    db.add(new); db.commit(); db.refresh(new)
    return new

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usr = db.query(models.User).filter(models.User.email == form.username).first()
    if not usr or not verify_password(form.password, usr.hashed_password):
        raise HTTPException(401, "Invalid creds")
    token = create_access_token({"sub": usr.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def me(user=Depends(get_current_user)):
    return user

@router.post("/leave", response_model=schemas.LeaveRequestOut)
def create_leave(req: schemas.LeaveRequestCreate, user=Depends(get_current_user), db=Depends(get_db)):
    lr = models.LeaveRequest(employee_id=user.id, **req.dict())
    db.add(lr); db.commit(); db.refresh(lr)
    return lr

@router.get("/my-leaves", response_model=List[schemas.LeaveRequestOut])
def my_leaves(user=Depends(get_current_user), db=Depends(get_db)):
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.employee_id == user.id).all()

@router.get("/salary", response_model=List[schemas.SalarySlipOut])
def get_salaries(user=Depends(get_current_user), db=Depends(get_db)):
    slips = db.query(models.SalarySlip).filter(models.SalarySlip.employee_id == user.id).all()
    return [{"id": s.id, "month": s.month, "download_url": f"/files/{s.file_path}"} for s in slips]

@router.get("/pulse", response_model=schemas.PulseBreakdown)
def pulse(user=Depends(get_current_user), db=Depends(get_db)):

    return schemas.PulseBreakdown(punctuality=80, attendance=90, feedback=85, overall=85.0)

@router.get("/badges", response_model=List[schemas.BadgeOut])
def badges(user=Depends(get_current_user), db=Depends(get_db)):
    bds = db.query(models.Badge).filter(models.Badge.employee_id == user.id).all()
    return bds

@router.get("/onboarding-progress", response_model=schemas.OnboardingProgress)
def onboarding(user=Depends(get_current_user)):
    steps = ["Upload ID", "Submit Bank", "Induction"]
    done = steps[:2]  
    return schemas.OnboardingProgress(completed_steps=done, total_steps=len(steps))

@router.get("/rank", response_model=schemas.TeamRank)
def rank(user=Depends(get_current_user)):

    return schemas.TeamRank(team="Alpha", rank=3, total_teams=5)
