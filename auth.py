from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, Token, UserOut
from database import get_db
from crud import get_user_by_username, get_user_by_email, create_user, authenticate_user
from deps import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/signup", response_model=UserOut)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    user = create_user(db, payload.username, payload.email, payload.password, payload.name, payload.role)
    return user

@router.post("/token", response_model=Token)
def login_for_token(form_data: dict, db: Session = Depends(get_db)):
    # form_data expected to be {"username": "...", "password":"..."}
    username = form_data.get("username")
    password = form_data.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="Missing username or password")
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_me(current_user = Depends(lambda: None)):
    # This endpoint will be replaced by main dependency injection on server runtime.
    # Include it in main by using get_current_user dependency. Placeholder here.
    raise HTTPException(status_code=501, detail="Use /users/me in the main app with dependency injection")
