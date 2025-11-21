from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os
class Settings(BaseSettings):
    # Proje Ayarları
    PROJECT_NAME: str = "Scalable E-Commerce API"
    VERSION: str = "1.0.0"
    
    # Veritabanı Ayarları (Docker compose'daki değerlerle aynı olmalı)
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "ecommerce_db"
    SECRET_KEY: str = "supersecretkey12345" # Gerçek projede bunu çok karmaşık yapmalısın
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Otomatik URL oluşturma
    @property
    def DATABASE_URL(self) -> str:
        # os.getenv ile ortam değişkenini kontrol ediyoruz
        import os
        url = os.getenv("DATABASE_URL")
        if url and url.startswith("postgres://"):
            # SQLAlchemy "postgres://" kabul etmez, "postgresql://" yapmamız lazım
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            return url

        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = ConfigDict(env_file=".env")
    
settings = Settings()