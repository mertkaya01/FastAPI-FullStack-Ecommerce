# 🚀 Scalable E-Commerce API

Bu proje, modern web teknolojileri ve temiz kod mimarisi kullanılarak geliştirilmiş, ölçeklenebilir bir E-Ticaret Backend API'sıdır.

## 🛠️ Teknolojiler ve Mimari

* **Backend:** Python 3.11, FastAPI (Asenkron Mimari)
* **Veritabanı:** PostgreSQL (AsyncPG Sürücüsü ile)
* **ORM:** SQLAlchemy 2.0 (Async)
* **Containerization:** Docker & Docker Compose
* **Authentication:** JWT (JSON Web Token) & OAuth2
* **Validation:** Pydantic v2

## 🌟 Temel Özellikler

* **Kullanıcı Yönetimi:** Güvenli kayıt (Password Hashing/Bcrypt) ve JWT tabanlı kimlik doğrulama.
* **Ürün & Kategori Yönetimi:** İlişkisel veritabanı yapısı (One-to-Many Relations).
* **Sipariş Sistemi:** Transaction yönetimi ile tutarlı sipariş oluşturma.
* **Stok Takibi:** Sipariş verildiğinde otomatik stok düşme (Business Logic).
* **Dockerize Ortam:** Tek komutla (`docker-compose up`) tüm altyapının ayağa kalkması.
## 🛠️ Admin Paneli Özellikleri

Yöneticiler için geliştirilen özel panel (`/frontend/admin.html`) üzerinden şu işlemler yapılabilir:

* **Dashboard:** Tüm ürünlerin stok durumunu ve kayıtlı üyeleri tek ekranda görüntüleme.
* **Stok Takibi:** Stoğu azalan ürünler (Stock < 5) otomatik olarak kırmızı ile vurgulanır.
* **Ürün Yönetimi:**
    * Yeni ürün ekleme (Modal Form).
    * Ürün silme (Güvenli Silme: Siparişi olan ürünler silinemez, kullanıcı uyarılır).
* **Sipariş Geçmişi:** Gelen tüm siparişlerin içeriğini ve tutarını tablolama.

## 🚀 Kurulum (Nasıl Çalıştırılır?)

Proje **Docker** üzerinde çalışacak şekilde tasarlanmıştır.

1.  **Repoyu klonlayın:**
    ```bash
    git clone [https://github.com/kullaniciadi/ecommerce-api.git](https://github.com/kullaniciadi/ecommerce-api.git)
    cd ecommerce-api
    ```

2.  **Docker ile başlatın:**
    ```bash
    docker compose up -d
    ```

3.  **API Dokümantasyonuna Gidin:**
    Tarayıcıda `http://localhost:8000/docs` adresine giderek Swagger UI üzerinden tüm sistemi test edebilirsiniz.

## 🧪 API Endpoint'leri

| Metod | Endpoint     | Açıklama                |
| :--- | :---         | :---                    |
| POST | `/login`     | Token almak için giriş  |
| POST | `/users`     | Yeni kullanıcı kaydı    |
| GET  | `/products`  | Ürünleri listele        |
| POST | `/orders`    | Sipariş oluştur (Auth)  |

---
*Computer Engineering Senior Project - 2025*

// Some Terminal tips for new users:
- docker compose down -v //
- docker compose up -d // restart the database
- python -m uvicorn app.main:app --reload  // start the http://127.0.0.1:8000/docs website.
