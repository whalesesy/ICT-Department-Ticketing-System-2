from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class RoleEnum(str, enum.Enum):
    user = "user"
    approver = "approver"
    admin = "admin"

class RequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    issued = "issued"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    name = Column(String(120), nullable=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    requests = relationship("Request", back_populates="requester")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(50), unique=True, index=True, nullable=False)
    type = Column(String(80), nullable=False)
    model = Column(String(120), nullable=True)
    status = Column(String(40), default="Available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    request_code = Column(String(50), unique=True, index=True, nullable=False)
    device = Column(String(80), nullable=False)
    quantity = Column(Integer, default=1)
    purpose = Column(Text, nullable=True)
    duration = Column(String(60), nullable=True)
    needed_by = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.pending)
    reject_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    requester_id = Column(Integer, ForeignKey("users.id"))
    requester = relationship("User", back_populates="requests")
