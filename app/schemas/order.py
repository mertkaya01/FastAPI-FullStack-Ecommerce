from pydantic import BaseModel
from typing import List
from pydantic import BaseModel, ConfigDict # Import ekle
from typing import List

# Kullanıcıdan gelen tekil ürün verisi
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

# Sipariş oluşturma isteği (Liste halinde ürünler)
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

# --- Response (Cevap) Modelleri ---

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float
    
    model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
    id: int
    total_amount: float
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)