from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import get_password_hash
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Bu email daha önce kayıt olmuş mu kontrol et
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı.")

    # 2. Şifreyi hashle
    hashed_password = get_password_hash(user.password)

    # 3. Yeni kullanıcı objesini oluştur
    new_user = User(
        email=user.email,
        password=hashed_password, # Düz şifreyi değil, hashli halini kaydediyoruz!
        is_active=True
    )

    # 4. Veritabanına ekle
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user) # ID bilgisini almak için veriyi yenile


    
    return new_user

@router.get("/", response_model=List[UserOut])
async def get_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Tüm kullanıcıları veritabanından çek
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()