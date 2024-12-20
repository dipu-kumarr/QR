from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.utils.qr_generator import generate_qr

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=UserResponse)
async def get_user(mobile: str = None, id: int = None, db: AsyncSession = Depends(get_db)):
    if mobile:
        query = await db.execute(f"SELECT * FROM users WHERE mobile='{mobile}'")
    elif id:
        query = await db.execute(f"SELECT * FROM users WHERE id={id}")
    else:
        raise HTTPException(status_code=400, detail="Provide either 'mobile' or 'id'")
    
    user = query.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if mobile number exists
    query = await db.execute(f"SELECT * FROM users WHERE mobile='{user.mobile}'")
    if query.scalar():
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    new_user = User(name=user.name, age=user.age, address=user.address, mobile=user.mobile)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Generate QR Code
    generate_qr(new_user.id)

    return new_user
