from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import DeviceCreate, DeviceOut
from crud import create_device, get_device_by_device_id, list_devices, update_device_status, delete_device
from deps import get_current_user, require_role

router = APIRouter()

# List devices (any authenticated user)
@router.get("/", response_model=List[DeviceOut])
def devices(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_devices(db)

# Admin: add device
@router.post("/", response_model=DeviceOut, dependencies=[Depends(require_role("admin"))])
def add_device(payload: DeviceCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if get_device_by_device_id(db, payload.device_id):
        raise HTTPException(400, "Device id already exists")
    d = create_device(db, payload.device_id, payload.type, payload.model, payload.status)
    return d

# Admin: update device status
@router.patch("/{device_id}/status", dependencies=[Depends(require_role("admin"))])
def change_status(device_id: str, payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    status = payload.get("status")
    device = get_device_by_device_id(db, device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    update_device_status(db, device, status)
    return {"message": "Updated"}

# Admin: delete device
@router.delete("/{device_id}", dependencies=[Depends(require_role("admin"))])
def remove_device(device_id: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    device = get_device_by_device_id(db, device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    delete_device(db, device)
    return {"message": "Deleted"}
