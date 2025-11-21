from contextlib import asynccontextmanager
from app.routers import user as user_router
from app.routers import auth as auth_router
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, engine, Base
from app.routers import auth as auth_router
from app.routers import product as product_router
from app.routers import order as order_router
from app.models import product
from app.models import order
from app.models import user # Modeli import etmezsek tablo oluşmaz!
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware



# --- Lifespan: Uygulama Başlarken Çalışacak Kodlar ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Tablolar oluşturuluyor...")
    async with engine.begin() as conn:
        # Veritabanında olmayan tabloları oluşturur
        await conn.run_sync(Base.metadata.create_all)
    print("Tablolar hazır!")
    yield

app = FastAPI(title="Scalable E-Commerce API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- CORS AYARLARI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerçek projede sadece kendi domainini yazmalısın
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, DELETE vb. hepsine izin ver
    allow_headers=["*"],
)
# ---------------------
# --- ROUTERLAR ---

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}