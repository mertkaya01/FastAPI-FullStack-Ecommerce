from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderOut, OrderItemOut
from sqlalchemy.orm import selectinload
from typing import List
from app.routers.auth import get_current_user # Giriş yapmış kullanıcıyı alacağız

# Not: get_current_user fonksiyonunu auth.py içinde tanımlamamız gerekebilir, 
# eğer yoksa aşağıda düzelteceğiz. Şimdilik böyle yazalım.

router = APIRouter(tags=["Orders"])

@router.post("/orders/", response_model=OrderOut)
async def create_order(
    order_in: OrderCreate, 
    current_user: User = Depends(get_current_user), # Sadece giriş yapanlar sipariş verebilir
    db: AsyncSession = Depends(get_db)
):
    total_amount = 0.0
    order_items = []

    # 1. Siparişteki her ürünü kontrol et
    for item in order_in.items:
        product = await db.get(Product, item.product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Ürün ID {item.product_id} bulunamadı")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"{product.name} için yeterli stok yok")

        # 2. Stok düş ve ara toplama ekle
        product.stock -= item.quantity
        total_amount += product.price * item.quantity
        
        # 3. Sipariş detayını listeye ekle (Henüz DB'ye yazmadık)
        new_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price=product.price
        )
        order_items.append(new_item)

    # 4. Ana siparişi oluştur
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        items=order_items # İlişki sayesinde hepsini tek seferde kaydeder
    )

    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    return OrderOut(
        id=new_order.id,
        total_amount=new_order.total_amount,
        items=[
            OrderItemOut(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price
            ) for item in order_items
        ]
    )
    # --- ADMIN İÇİN: TÜM SİPARİŞLERİ LİSTELE ---
@router.get("/orders/all", response_model=List[OrderOut])
async def get_all_orders(db: AsyncSession = Depends(get_db)):
    # Siparişleri ve içindeki ürünleri getir
    result = await db.execute(
        select(Order).options(selectinload(Order.items))
    )
    return result.scalars().all()
    return new_order

