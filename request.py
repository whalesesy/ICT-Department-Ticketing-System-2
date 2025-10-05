from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import RequestCreate, RequestOut
from crud import create_request, list_requests_for_user, list_pending_requests, get_request, update_request_status
from deps import get_current_user, require_role
from models import RequestStatus

router = APIRouter()

# Create a new request (authenticated user)
@router.post("/", response_model=RequestOut)
def submit_request(payload: RequestCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    req = create_request(db, current_user, payload.device, payload.quantity, payload.purpose or "", payload.duration or "", payload.needed_by)
    return req

# List my requests
@router.get("/me", response_model=List[RequestOut])
def my_requests(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_requests_for_user(db, current_user.id)

# List pending approvals (approver or admin)
@router.get("/pending", response_model=List[RequestOut], dependencies=[Depends(require_role("approver"))])
def pending_requests(db: Session = Depends(get_db)):
    return list_pending_requests(db)

# Approve a request (approver/admin)
@router.post("/{request_id}/approve", dependencies=[Depends(require_role("approver"))])
def approve_request(request_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    r = get_request(db, request_id)
    if not r:
        raise HTTPException(404, "Request not found")
    update_request_status(db, r, RequestStatus.approved)
    return {"message": f"Request {r.request_code} approved"}

# Reject a request (approver/admin)
@router.post("/{request_id}/reject", dependencies=[Depends(require_role("approver"))])
def reject_request(request_id: int, payload: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # payload should include {"reason": "text"}
    reason = payload.get("reason", "")
    r = get_request(db, request_id)
    if not r:
        raise HTTPException(404, "Request not found")
    update_request_status(db, r, RequestStatus.rejected, reject_reason=reason)
    return {"message": f"Request {r.request_code} rejected"}
