from pydantic import BaseModel
from typing import List, Optional
from pydantic import BaseModel, ConfigDict # Import ekle
from typing import List, Optional



# --- CATEGORY SCHEMAS ---
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    is_active: bool
    # İstersen ürünün içine kategori bilgisini de gömebiliriz
    category: CategoryOut 
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)