from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.core.enums import RoleEnum, LeaveStatusEnum
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.employee)
    name = Column(String)

    leaves = relationship("LeaveRequest", back_populates="employee")
    salaries = relationship("SalarySlip", back_populates="employee")
    badges = relationship("Badge", back_populates="employee")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(String)
    end_date = Column(String)
    reason = Column(String)
    status = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.pending)
    created_at = Column(DateTime, default=datetime.utcnow)

    employee = relationship("User", back_populates="leaves")

class SalarySlip(Base):
    __tablename__ = "salary_slips"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    month = Column(String)
    file_path = Column(String) 

    employee = relationship("User", back_populates="salaries")

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    date_awarded = Column(DateTime, default=datetime.utcnow)

    employee = relationship("User", back_populates="badges")
