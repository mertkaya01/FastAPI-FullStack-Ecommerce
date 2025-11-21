import pytest

# Bu dekoratör, testin asenkron (async) çalışmasını sağlar
@pytest.mark.asyncio
async def test_create_category(client):
    # 1. Kategori oluşturma isteği gönder
    response = await client.post(
        "/categories/",
        json={"name": "Knives"}
    )
    
    # 2. Durum kodu 200 mü? (Başarılı mı?)
    assert response.status_code == 200
    
    # 3. Gelen veriyi kontrol et
    data = response.json()
    assert data["name"] == "Knives"
    assert "id" in data # ID oluşmuş mu?

@pytest.mark.asyncio
async def test_create_category_duplicate(client):
    # 1. İlk kategoriyi oluştur
    await client.post("/categories/", json={"name": "Ayni İsim"})
    
    # 2. Aynı isimle TEKRAR oluşturmaya çalış
    response = await client.post("/categories/", json={"name": "Ayni İsim"})
    
    # 3. Beklenen: 400 Bad Request (Çünkü isimler benzersiz olmalı!)
    assert response.status_code == 400