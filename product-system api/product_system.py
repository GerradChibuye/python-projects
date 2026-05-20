from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

products = [
    {"id": 1, "name": "Gaming Laptop", "brand": "ASUS ROG", "price": 18500.00, "category": "Laptops", "stock": 15, "rating": 4.8},
    {"id": 2, "name": "Wireless Mouse", "brand": "Logitech", "price": 750.00, "category": "Accessories", "stock": 50, "rating": 4.5},
    {"id": 3, "name": "Mechanical Keyboard", "brand": "Corsair", "price": 2100.00, "category": "Accessories", "stock": 30, "rating": 4.7},
    {"id": 4, "name": "27-inch Monitor", "brand": "Dell", "price": 4800.00, "category": "Displays", "stock": 12, "rating": 4.6},
    {"id": 5, "name": "Noise Cancelling Headphones", "brand": "Sony", "price": 3200.00, "category": "Audio", "stock": 25, "rating": 4.9},
    {"id": 6, "name": "External SSD 1TB", "brand": "Samsung", "price": 1450.00, "category": "Storage", "stock": 40, "rating": 4.4}
]

def find_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return product
    return None

@app.route('/api/products', methods=['GET'])
def get_all_products():
    return jsonify(products), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_one_product(product_id):
    product = find_product(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product), 200

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    if "name" not in data:
        return jsonify({"error": "Product name is required"}), 400
    
    if "price" not in data:
        return jsonify({"error": "Product price is required"}), 400
    
    new_id = 1
    for product in products:
        if product["id"] >= new_id:
            new_id = product["id"] + 1
    
    new_product = {
        "id": new_id,
        "name": data["name"],
        "brand": data.get("brand", "Unknown"),
        "price": float(data["price"]),
        "category": data.get("category", "General"),
        "stock": data.get("stock", 0),
        "rating": data.get("rating", 0.0)
    }
    
    products.append(new_product)
    return jsonify(new_product), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = find_product(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No JSON data provided"}), 400
    
    if "name" in data:
        product["name"] = data["name"]
    if "brand" in data:
        product["brand"] = data["brand"]
    if "price" in data:
        product["price"] = data["price"]
    if "category" in data:
        product["category"] = data["category"]
    if "stock" in data:
        product["stock"] = data["stock"]
    if "rating" in data:
        product["rating"] = data["rating"]
    
    return jsonify(product), 200

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    product = find_product(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    
    new_products = []
    for p in products:
        if p["id"] != product_id:
            new_products.append(p)
    products = new_products
    
    return jsonify({"message": "Product deleted successfully"}), 200

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechShop Zambia - Inventory System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f0f2f5;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            color: #1a2a3a;
            margin-bottom: 10px;
            font-size: 28px;
        }

        .subtitle {
            text-align: center;
            color: #4a5568;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1.5fr;
            gap: 20px;
        }

        .form-panel {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .form-panel h2 {
            color: #1a2a3a;
            margin-bottom: 20px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 20px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
            font-size: 14px;
        }

        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }

        input:focus {
            outline: none;
            border-color: #3498db;
        }

        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            margin-right: 10px;
            margin-top: 10px;
        }

        button:hover {
            background-color: #2980b9;
        }

        .btn-cancel {
            background-color: #95a5a6;
        }

        .btn-cancel:hover {
            background-color: #7f8c8d;
        }

        .products-panel {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .products-panel h2 {
            color: #1a2a3a;
            margin-bottom: 20px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 20px;
        }

        .search-box {
            margin-bottom: 20px;
        }

        .search-box input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }

        .product-card {
            background: #f9f9f9;
            border-left: 3px solid #3498db;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }

        .product-name {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }

        .product-details {
            font-size: 13px;
            color: #7f8c8d;
            margin-top: 8px;
        }

        .product-price {
            color: #27ae60;
            font-weight: bold;
            font-size: 18px;
            margin-top: 5px;
        }

        .stock-badge {
            display: inline-block;
            background: #ecf0f1;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 10px;
        }

        .product-actions {
            margin-top: 10px;
        }

        .edit-btn {
            background-color: #3498db;
            padding: 5px 10px;
            font-size: 12px;
            margin-right: 8px;
        }

        .delete-btn {
            background-color: #e74c3c;
            padding: 5px 10px;
            font-size: 12px;
        }

        .delete-btn:hover {
            background-color: #c0392b;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #7f8c8d;
        }

        .message {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            display: none;
            z-index: 1000;
        }

        .message.error {
            background: #e74c3c;
        }

        .stats {
            background: #ecf0f1;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            text-align: center;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>TechShop Zambia</h1>
        <div class="subtitle">Inventory Management System</div>

        <div class="dashboard">
            <div class="form-panel">
                <h2 id="form-title">Add New Product</h2>
                <form id="product-form">
                    <input type="hidden" id="product-id">
                    
                    <div class="form-group">
                        <label>Product Name *</label>
                        <input type="text" id="name" required placeholder="Enter product name">
                    </div>
                    
                    <div class="form-group">
                        <label>Brand</label>
                        <input type="text" id="brand" placeholder="Enter brand name">
                    </div>
                    
                    <div class="form-group">
                        <label>Price (ZMW) *</label>
                        <input type="number" step="0.01" id="price" required placeholder="Enter price">
                    </div>
                    
                    <div class="form-group">
                        <label>Category</label>
                        <select id="category">
                            <option value="Laptops">Laptops</option>
                            <option value="Accessories">Accessories</option>
                            <option value="Displays">Displays</option>
                            <option value="Audio">Audio</option>
                            <option value="Storage">Storage</option>
                            <option value="General">General</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Stock Quantity</label>
                        <input type="number" id="stock" value="0">
                    </div>
                    
                    <div class="form-group">
                        <label>Rating (0-5)</label>
                        <input type="number" step="0.1" id="rating" value="0">
                    </div>
                    
                    <button type="submit">Save Product</button>
                    <button type="button" class="btn-cancel" onclick="resetForm()">Cancel</button>
                </form>
            </div>

            <div class="products-panel">
                <h2>Product Inventory</h2>
                <div class="stats" id="stats">
                    Loading...
                </div>
                <div class="search-box">
                    <input type="text" id="search" placeholder="Search products by name or brand..." onkeyup="filterProducts()">
                </div>
                <div id="products-list">
                    <div class="loading">Loading products...</div>
                </div>
            </div>
        </div>
    </div>

    <div id="message" class="message"></div>

    <script>
        const API_URL = '/api/products';
        let allProducts = [];

        function showMessage(text, isError = false) {
            const msg = document.getElementById('message');
            msg.textContent = text;
            msg.className = isError ? 'message error' : 'message';
            msg.style.display = 'block';
            setTimeout(function() {
                msg.style.display = 'none';
            }, 3000);
        }

        async function fetchProducts() {
            try {
                const response = await fetch(API_URL);
                if (!response.ok) {
                    throw new Error('Failed to fetch');
                }
                allProducts = await response.json();
                displayProducts(allProducts);
                updateStats();
            } catch (error) {
                showMessage('Cannot connect to server. Make sure Flask is running!', true);
                document.getElementById('products-list').innerHTML = '<div class="loading">Error: Cannot connect to API</div>';
            }
        }

        function updateStats() {
            let totalProducts = allProducts.length;
            let totalStock = 0;
            let totalRating = 0;
            
            for (let i = 0; i < allProducts.length; i++) {
                totalStock = totalStock + allProducts[i].stock;
                totalRating = totalRating + allProducts[i].rating;
            }
            
            let avgRating = (totalRating / totalProducts).toFixed(1);
            if (totalProducts === 0) {
                avgRating = 0;
            }
            
            document.getElementById('stats').innerHTML = 'Total Products: ' + totalProducts + ' | Total Stock: ' + totalStock + ' | Average Rating: ' + avgRating + '/5';
        }

        function displayProducts(products) {
            const container = document.getElementById('products-list');
            if (products.length === 0) {
                container.innerHTML = '<div class="loading">No products found</div>';
                return;
            }

            let html = '';
            for (let i = 0; i < products.length; i++) {
                let product = products[i];
                html = html + `
                    <div class="product-card">
                        <div class="product-name">
                            ${product.name}
                            <span class="stock-badge">Stock: ${product.stock}</span>
                        </div>
                        <div class="product-details">
                            Brand: ${product.brand} | Category: ${product.category} | Rating: ${product.rating}/5
                        </div>
                        <div class="product-price">
                            K${product.price.toLocaleString()}
                        </div>
                        <div class="product-actions">
                            <button class="edit-btn" onclick="editProduct(${product.id})">Edit</button>
                            <button class="delete-btn" onclick="deleteProduct(${product.id})">Delete</button>
                        </div>
                    </div>
                `;
            }
            container.innerHTML = html;
        }

        function filterProducts() {
            let searchTerm = document.getElementById('search').value.toLowerCase();
            let filtered = [];
            
            for (let i = 0; i < allProducts.length; i++) {
                let product = allProducts[i];
                if (product.name.toLowerCase().includes(searchTerm) || product.brand.toLowerCase().includes(searchTerm)) {
                    filtered.push(product);
                }
            }
            
            displayProducts(filtered);
        }

        function editProduct(id) {
            let product = null;
            for (let i = 0; i < allProducts.length; i++) {
                if (allProducts[i].id === id) {
                    product = allProducts[i];
                    break;
                }
            }
            
            if (product) {
                document.getElementById('product-id').value = product.id;
                document.getElementById('name').value = product.name;
                document.getElementById('brand').value = product.brand;
                document.getElementById('price').value = product.price;
                document.getElementById('category').value = product.category;
                document.getElementById('stock').value = product.stock;
                document.getElementById('rating').value = product.rating;
                document.getElementById('form-title').innerHTML = 'Edit Product';
                
                document.querySelector('.form-panel').scrollIntoView({ behavior: 'smooth' });
            }
        }

        async function deleteProduct(id) {
            let confirmDelete = confirm('Are you sure you want to delete this product?');
            if (confirmDelete) {
                try {
                    let response = await fetch(API_URL + '/' + id, { method: 'DELETE' });
                    if (response.ok) {
                        showMessage('Product deleted successfully!');
                        fetchProducts();
                        resetForm();
                    } else {
                        showMessage('Failed to delete product', true);
                    }
                } catch (error) {
                    showMessage('Error deleting product', true);
                }
            }
        }

        async function saveProduct(productData, isUpdate, id) {
            let url = API_URL;
            let method = 'POST';
            
            if (isUpdate) {
                url = API_URL + '/' + id;
                method = 'PUT';
            }
            
            try {
                let response = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(productData)
                });
                
                if (response.ok) {
                    if (isUpdate) {
                        showMessage('Product updated!');
                    } else {
                        showMessage('Product created!');
                    }
                    fetchProducts();
                    resetForm();
                } else {
                    let error = await response.json();
                    showMessage(error.error || 'Operation failed', true);
                }
            } catch (error) {
                showMessage('Error saving product', true);
            }
        }

        document.getElementById('product-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            let id = document.getElementById('product-id').value;
            let productData = {
                name: document.getElementById('name').value,
                brand: document.getElementById('brand').value || 'Unknown',
                price: parseFloat(document.getElementById('price').value),
                category: document.getElementById('category').value,
                stock: parseInt(document.getElementById('stock').value) || 0,
                rating: parseFloat(document.getElementById('rating').value) || 0
            };
            
            if (!productData.name || !productData.price) {
                showMessage('Name and Price are required!', true);
                return;
            }
            
            if (id) {
                saveProduct(productData, true, id);
            } else {
                saveProduct(productData, false, null);
            }
        });

        function resetForm() {
            document.getElementById('product-form').reset();
            document.getElementById('product-id').value = '';
            document.getElementById('form-title').innerHTML = 'Add New Product';
        }

        fetchProducts();
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("\n" + "="*50)
    print("TechShop Zambia Inventory API is running!")
    print("Available endpoints:")
    print("   GET    /api/products           - Fetch all products")
    print("   GET    /api/products/{id}      - Fetch one product")
    print("   POST   /api/products           - Add new product")
    print("   PUT    /api/products/{id}      - Update product")
    print("   DELETE /api/products/{id}      - Remove product")
    print("="*50 + "\n")
    print("Current Products in Stock (Zambian Kwacha):")
    for product in products:
        print(f"   [{product['id']}] {product['name']} - K{product['price']:,.2f} - Stock: {product['stock']}")
    print("\n" + "="*50 + "\n")
    print("Open your browser and go to: http://localhost:5000")
    print("\n" + "="*50 + "\n")
    app.run(debug=True, port=5000)