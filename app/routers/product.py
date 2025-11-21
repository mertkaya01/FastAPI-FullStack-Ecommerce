from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from typing import List
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from sqlalchemy.exc import IntegrityError
from app.models.product import Category, Product
from app.schemas.product import CategoryCreate, CategoryOut, ProductCreate, ProductOut
from sqlalchemy.exc import IntegrityError
import shutil
import os
import uuid
from fastapi import File, UploadFile, Form

router = APIRouter(tags=["Products & Categories"])

# --- KATEGORİ İŞLEMLERİ ---

@router.post("/categories/", response_model=CategoryOut)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Aynı isimde kategori var mı kontrol et
    result = await db.execute(select(Category).where(Category.name == category.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Bu kategori zaten var.")
    
    new_category = Category(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

@router.get("/products/", response_model=List[ProductOut])
async def get_products(
    db: AsyncSession = Depends(get_db),
    q: Optional[str] = None,  # Arama kelimesi (Opsiyonel)
    skip: int = 0,            # Kaç kayıt atlanacak? (Sayfalama için)
    limit: int = 10           # Kaç kayıt getirilecek? (Varsayılan 10)
):
    
    query = select(Product).options(selectinload(Product.category))
    
    if q:
        # 'ilike': Büyük/küçük harf duyarsız arama yapar (Apple = apple)
        # %q%: Kelimenin içinde geçmesi yeterli (SQL LIKE mantığı)
        query = query.where(Product.name.ilike(f"%{q}%"))
    
    query = query.offset(skip).limit(limit)
    
    # selectinload: Veritabanına "Ürünleri getirirken Kategorilerini de paketle" diyoruz.
    result = await db.execute(query)
    return result.scalars().all()

# --- ÜRÜN İŞLEMLERİ ---

@router.post("/products/", response_model=ProductOut)
async def create_product(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(None), # Resim dosyası (Opsiyonel)
    db: AsyncSession = Depends(get_db)
):
    # 1. Kategori kontrolü
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Kategori bulunamadı.")

    # 2. Resim Yükleme İşlemi
    image_url = None
    if file:
        file_extension = file.filename.split(".")[-1]
        new_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # --- YENİ EKLENECEK KISIM BAŞLANGICI ---
        # Klasör yolunu tanımla
        upload_dir = "static/image"
        
        # Klasör yoksa oluştur (Garanti Yöntem)
        os.makedirs(upload_dir, exist_ok=True)
        # ---------------------------------------

        file_location = f"{upload_dir}/{new_filename}"
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        image_url = f"/{upload_dir}/{new_filename}"

    # 3. Ürünü Oluştur
    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
        image_url=image_url # Resim yolunu kaydet
    )
    
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    
    # Pydantic için manuel paketleme
    return ProductOut(
        id=new_product.id,
        name=new_product.name,
        description=new_product.description,
        price=new_product.price,
        stock=new_product.stock,
        is_active=new_product.is_active,
        category_id=new_product.category_id,
        image_url=new_product.image_url,
        category=CategoryOut(id=category.id, name=category.name)
    )
    
@router.get("/products/", response_model=List[ProductOut])
async def get_products(db: AsyncSession = Depends(get_db)):
    # Ürünleri getirirken ilişkili olduğu kategoriyi de yükle (Eager Loading)
    # Not: Şimdilik basit tutuyoruz, ileride 'joinedload' ekleyebiliriz.
    result = await db.execute(select(Product))
    return result.scalars().all()

@router.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    # 1. Ürünü Bul
    product = await db.get(Product, product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

    # 2. Silmeyi Dene
    try:
        await db.delete(product)
        await db.commit()
    except IntegrityError:
        # Veritabanı "Silemezsin!" derse buraya düşer
        await db.rollback() # İşlemi geri al ki veritabanı kilitlenmesin
        raise HTTPException(
            status_code=400, 
            detail="Bu ürün bir siparişte yer aldığı için SİLİNEMEZ! Önce siparişi iptal etmelisiniz."
        )
    except Exception as e:
        # Başka bir hata olursa (Güvenlik ağı)
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Beklenmedik hata: {str(e)}")
    
    return None