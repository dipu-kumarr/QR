from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/qr", tags=["QR"])

@router.get("/{user_id}", response_model=dict)
async def get_user_by_qr(user_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(f"SELECT * FROM users WHERE id={user_id}")
    user = query.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "age": user.age, "address": user.address, "mobile": user.mobile}
