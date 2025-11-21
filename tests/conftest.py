import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# 1. Test için geçici bir SQLite veritabanı kullan (RAM'de çalışır, çok hızlıdır)
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # SQLite için gerekli ayar
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine, class_=AsyncSession
)

# 2. Her testten önce tabloları oluştur, sonra sil
@pytest.fixture(scope="function")
async def async_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
        
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# 3. Uygulamanın "get_db" bağımlılığını test veritabanıyla değiştir (Override)
@pytest.fixture(scope="function")
async def client(async_db):
    async def override_get_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_db
    
    # Testler için sanal bir istemci (Browser gibi davranır) oluştur
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    
    app.dependency_overrides.clear()