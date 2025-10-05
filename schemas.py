from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from models import RoleEnum, RequestStatus

# -- Users
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    name: Optional[str] = None
    role: Optional[RoleEnum] = RoleEnum.user

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: Optional[str] = None
    role: RoleEnum

    class Config:
        orm_mode = True

# -- Token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# -- Requests
class RequestCreate(BaseModel):
    device: str
    quantity: int = 1
    purpose: Optional[str] = None
    duration: Optional[str] = None
    needed_by: Optional[datetime] = None

class RequestOut(BaseModel):
    id: int
    request_code: str
    device: str
    quantity: int
    purpose: Optional[str]
    duration: Optional[str]
    needed_by: Optional[datetime]
    status: RequestStatus
    reject_reason: Optional[str]
    requester_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# -- Device
class DeviceCreate(BaseModel):
    device_id: str
    type: str
    model: Optional[str] = None
    status: Optional[str] = "Available"

class DeviceOut(BaseModel):
    id: int
    device_id: str
    type: str
    model: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
