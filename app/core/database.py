from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Veritabanı Motorunu Oluştur (Async)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. Oturum (Session) Fabrikasını Kur
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False,
    bind=engine, 
    class_=AsyncSession
)

# 3. Veritabanı Modelleri için Temel Sınıf
Base = declarative_base()

# 4. Dependency (Her istekte DB açıp kapatan fonksiyon)
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()