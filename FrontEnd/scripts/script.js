document.addEventListener("DOMContentLoaded", () => {
    showSkeleton();
    loadProducts();
});

/* ---------------- Skeleton Loader ---------------- */
function showSkeleton() {
    const container = document.getElementById("product-list");
    container.innerHTML = "";

    for (let i = 0; i < 6; i++) {
        container.innerHTML += `
            <div class="col-md-4">
                <div class="skeleton skeleton-card"></div>
            </div>
        `;
    }
}

/* ---------------- Load Products from API ---------------- */
async function loadProducts() {
    const productList = document.getElementById("product-list");

    try {
        const response = await fetch("http://127.0.0.1:8000/products/");
        const products = await response.json();

        productList.innerHTML = "";

        products.forEach(p => {
            productList.innerHTML += createProductCard(p);
        });
    }
    catch (e) {
        productList.innerHTML = `
            <div class="alert alert-danger">
                Sunucuya bağlanılamadı! Backend çalışıyor mu?
            </div>`;
    }
}

/* ---------------- Product Card Template ---------------- */
function createProductCard(product) {
    return `
        <div class="col-md-4 mb-4">
            <div class="card">
                <img src="https://via.placeholder.com/300" alt="${product.name}">

                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="text-muted">${product.description || "Açıklama yok"}</p>

                    <div class="d-flex justify-content-between align-items-center">
                        <span class="price-tag">${product.price} ₺</span>
                        <span class="badge bg-success">Stok: ${product.stock}</span>
                    </div>

                    <button class="btn btn-outline-primary btn-add w-100 mt-3"
                            onclick="addToCart(${product.id})">
                        Sepete Ekle
                    </button>
                </div>
            </div>
        </div>
    `;
}

/* ---------------- Cart System ---------------- */
function addToCart(id) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    cart.push(id);
    localStorage.setItem("cart", JSON.stringify(cart));

    alert("Ürün sepete eklendi!");
}
