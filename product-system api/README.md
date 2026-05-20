# TechShop Zambia - Product Management System

A full-stack Flask-based inventory management system for managing tech products with a responsive web interface.

## 📋 Overview

TechShop Zambia is a web application designed to help manage product inventory for a technology retail business. It provides a REST API backend and an interactive web interface for performing CRUD operations on products.

**Currency**: All prices are in Zambian Kwacha (ZMW)

## ✨ Features

- **Product Management**: Create, Read, Update, and Delete (CRUD) products
- **Real-time Search**: Filter products by name or brand
- **Inventory Tracking**: Monitor stock levels for each product
- **Product Rating**: Track and display product ratings (0-5 scale)
- **Dashboard Statistics**: View total products, total stock, and average rating
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **RESTful API**: Complete REST API for programmatic access

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data Storage**: In-memory (Python list)

## 📁 File Structure

```
product-system api/
├── product_system.py     # Main application file
└── README.md            # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GerradChibuye/python-projects.git
   cd python-projects/product-system\ api
   ```

2. **Install Flask**:
   ```bash
   pip install flask
   ```

3. **Run the application**:
   ```bash
   python product_system.py
   ```

4. **Access the web interface**:
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## 📚 API Endpoints

### Get All Products
```
GET /api/products
```
Returns a list of all products in the inventory.

**Example Response**:
```json
[
  {
    "id": 1,
    "name": "Gaming Laptop",
    "brand": "ASUS ROG",
    "price": 18500.00,
    "category": "Laptops",
    "stock": 15,
    "rating": 4.8
  },
  ...
]
```

### Get Single Product
```
GET /api/products/{id}
```
Returns a specific product by ID.

**Example**: `GET /api/products/1`

**Response**:
```json
{
  "id": 1,
  "name": "Gaming Laptop",
  "brand": "ASUS ROG",
  "price": 18500.00,
  "category": "Laptops",
  "stock": 15,
  "rating": 4.8
}
```

### Create Product
```
POST /api/products
```
Adds a new product to the inventory.

**Required Fields**:
- `name` (string)
- `price` (number)

**Optional Fields**:
- `brand` (string, default: "Unknown")
- `category` (string, default: "General")
- `stock` (integer, default: 0)
- `rating` (number, default: 0.0)

**Example Request**:
```json
{
  "name": "USB-C Cable",
  "brand": "Anker",
  "price": 150.00,
  "category": "Accessories",
  "stock": 100,
  "rating": 4.6
}
```

**Response** (HTTP 201):
```json
{
  "id": 7,
  "name": "USB-C Cable",
  "brand": "Anker",
  "price": 150.00,
  "category": "Accessories",
  "stock": 100,
  "rating": 4.6
}
```

### Update Product
```
PUT /api/products/{id}
```
Updates an existing product.

**Example Request**:
```json
{
  "price": 160.00,
  "stock": 95
}
```

**Response** (HTTP 200):
```json
{
  "id": 7,
  "name": "USB-C Cable",
  "brand": "Anker",
  "price": 160.00,
  "category": "Accessories",
  "stock": 95,
  "rating": 4.6
}
```

### Delete Product
```
DELETE /api/products/{id}
```
Removes a product from the inventory.

**Example**: `DELETE /api/products/7`

**Response** (HTTP 200):
```json
{
  "message": "Product deleted successfully"
}
```

## 🏠 Web Interface

### Dashboard Layout

The web interface consists of two main panels:

#### Left Panel - Add/Edit Product Form
- **Product Name** (required)
- **Brand** (optional)
- **Price in ZMW** (required)
- **Category** dropdown (Laptops, Accessories, Displays, Audio, Storage, General)
- **Stock Quantity**
- **Rating** (0-5 scale)

#### Right Panel - Product Inventory
- **Search Bar**: Real-time filtering by product name or brand
- **Statistics**: Total products, total stock, and average rating
- **Product Cards**: Display each product with:
  - Product name and stock badge
  - Brand, category, and rating information
  - Price in ZMW
  - Edit and Delete buttons

## 📊 Available Products

The system comes pre-loaded with the following products:

| ID | Product Name | Brand | Price (ZMW) | Category | Stock | Rating |
|----|---|---|---|---|---|---|
| 1 | Gaming Laptop | ASUS ROG | 18,500.00 | Laptops | 15 | 4.8 |
| 2 | Wireless Mouse | Logitech | 750.00 | Accessories | 50 | 4.5 |
| 3 | Mechanical Keyboard | Corsair | 2,100.00 | Accessories | 30 | 4.7 |
| 4 | 27-inch Monitor | Dell | 4,800.00 | Displays | 12 | 4.6 |
| 5 | Noise Cancelling Headphones | Sony | 3,200.00 | Audio | 25 | 4.9 |
| 6 | External SSD 1TB | Samsung | 1,450.00 | Storage | 40 | 4.4 |

## 💡 Usage Examples

### Using the Web Interface

1. **Add a Product**:
   - Fill in the form on the left panel
   - Click "Save Product"
   - The new product will appear in the inventory list

2. **Search Products**:
   - Type in the search box on the right panel
   - Results filter in real-time

3. **Edit a Product**:
   - Click the "Edit" button on a product card
   - The form populates with the product's data
   - Modify as needed and click "Save Product"

4. **Delete a Product**:
   - Click the "Delete" button on a product card
   - Confirm the deletion when prompted

### Using cURL for API Requests

**Fetch all products**:
```bash
curl http://localhost:5000/api/products
```

**Add a new product**:
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Monitor Stand","brand":"Ergotron","price":1200,"category":"Accessories","stock":20,"rating":4.5}'
```

**Update a product**:
```bash
curl -X PUT http://localhost:5000/api/products/7 \
  -H "Content-Type: application/json" \
  -d '{"stock":25}'
```

**Delete a product**:
```bash
curl -X DELETE http://localhost:5000/api/products/7
```

## 🔄 How It Works

1. **Flask Backend**: Handles all HTTP requests and manages the product data in memory
2. **RESTful Routes**: Each endpoint corresponds to a specific operation
3. **Frontend JavaScript**: Communicates with the API, updates the UI dynamically
4. **In-Memory Storage**: Products are stored in a Python list (data is lost when the server stops)

## ⚠️ Notes

- **Data Persistence**: This application stores data in memory only. All changes are lost when the server is restarted.
- **Single User**: The system is designed for single-user or small team use. No authentication is implemented.
- **ID Generation**: Product IDs are auto-generated based on the highest existing ID + 1

## 🔮 Future Enhancements

Potential improvements for this system:

- Database integration (SQLite, PostgreSQL) for persistent data storage
- User authentication and role-based access control
- Product image upload and display
- Advanced filtering and sorting options
- Inventory low-stock alerts
- Sales history and analytics
- Customer reviews and detailed product descriptions
- Export to CSV/PDF functionality
- API pagination for large datasets
- Input validation and error handling improvements

## 📝 License

This project is part of a learning exercise. Feel free to use and modify as needed.

## 👤 Author

**Gerrad Chibuye**

GitHub: [@GerradChibuye](https://github.com/GerradChibuye)

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests

---

**Happy Product Management! 🛍️**
