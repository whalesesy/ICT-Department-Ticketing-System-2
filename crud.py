from sqlalchemy.orm import Session
from models import User, Device, Request, RoleEnum, RequestStatus
from passlib.hash import bcrypt
from typing import Optional
from datetime import datetime
import secrets

# --- Users
def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, username: str, email: str, password: str, name: Optional[str], role: RoleEnum) -> User:
    hashed = bcrypt.hash(password)
    user = User(username=username, email=email, hashed_password=hashed, name=name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)
    if not user: return None
    if not bcrypt.verify(password, user.hashed_password): return None
    return user

# --- Requests
def create_request(db: Session, requester: User, device: str, quantity: int, purpose: str, duration: str, needed_by: Optional[datetime]) -> Request:
    code = "REQ-" + secrets.token_hex(4).upper()
    req = Request(
        request_code=code,
        device=device,
        quantity=quantity,
        purpose=purpose,
        duration=duration,
        needed_by=needed_by,
        requester=requester,
        status=RequestStatus.pending
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def get_request(db: Session, request_id: int) -> Optional[Request]:
    return db.query(Request).filter(Request.id == request_id).first()

def list_requests_for_user(db: Session, user_id: int):
    return db.query(Request).filter(Request.requester_id == user_id).order_by(Request.created_at.desc()).all()

def list_pending_requests(db: Session):
    return db.query(Request).filter(Request.status == RequestStatus.pending).order_by(Request.created_at.desc()).all()

def update_request_status(db: Session, req: Request, status: RequestStatus, reject_reason: Optional[str] = None):
    req.status = status
    if reject_reason:
        req.reject_reason = reject_reason
    db.commit()
    db.refresh(req)
    return req

# --- Devices
def create_device(db: Session, device_id: str, type: str, model: Optional[str], status: str):
    d = Device(device_id=device_id, type=type, model=model, status=status)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

def get_device_by_device_id(db: Session, device_id: str):
    return db.query(Device).filter(Device.device_id == device_id).first()

def list_devices(db: Session):
    return db.query(Device).order_by(Device.created_at.desc()).all()

def update_device_status(db: Session, device: Device, status: str):
    device.status = status
    db.commit()
    db.refresh(device)
    return device

def delete_device(db: Session, device: Device):
    db.delete(device)
    db.commit()
