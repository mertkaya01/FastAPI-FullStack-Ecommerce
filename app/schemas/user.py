from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, EmailStr, ConfigDict # ConfigDict'i import etmeyi unutma!
# Kullanıcı oluştururken istenecek veriler
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Kullanıcıya veriyi gösterirken dönecek veriler (Şifre yok!)
class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)