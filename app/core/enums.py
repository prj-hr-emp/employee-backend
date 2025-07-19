from enum import Enum


class RoleEnum(str, Enum):
    employee = "employee"
    hr = "hr"


class LeaveStatusEnum(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
