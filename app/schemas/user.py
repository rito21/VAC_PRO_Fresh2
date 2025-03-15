from typing import ClassVar

from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    full_name: str
    company_id: int


class UserInfo(BaseModel):
    user_id: int
    email: EmailStr
    password: str
    full_name: str
    creation_date: datetime
    failed_login_attempts: int
    last_access_date: datetime
    is_locked: bool
    is_deleted: bool
    is_verified: bool
    company_id: int