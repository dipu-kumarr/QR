from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse
import qrcode
import os

router = APIRouter(prefix="/users", tags=["Users"])

# Create a user
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(name=user.name, email=user.email, phone=user.phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate QR Code
    qr_data = f"http://localhost:8000/users/{new_user.id}"
    qr_path = f"static/qrcodes/user_{new_user.id}.png"
    qr = qrcode.make(qr_data)
    os.makedirs(os.path.dirname(qr_path), exist_ok=True)
    qr.save(qr_path)

    return new_user

# Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get QR Code
@router.get("/{user_id}/qrcode")
def get_user_qr(user_id: int):
    qr_path = f"static/qrcodes/user_{user_id}.png"
    if not os.path.exists(qr_path):
        raise HTTPException(status_code=404, detail="QR Code not found")
    return {"qr_code_url": f"http://localhost:8000/{qr_path}"}
