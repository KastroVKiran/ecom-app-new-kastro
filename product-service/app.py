from flask import Flask, render_template, request, jsonify
import pymongo
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://admin:password@localhost:27017/ecommerce_db')
client = pymongo.MongoClient(MONGODB_URI)
db = client.ecommerce_db
products_collection = db.products

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "product-service"})

@app.route('/products', methods=['GET'])
def get_products():
    products = list(products_collection.find({}, {'_id': 0}))
    return jsonify(products)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    product = {
        'name': data['name'],
        'description': data['description'],
        'price': float(data['price']),
        'category': data['category'],
        'stock': int(data['stock']),
        'image_url': data.get('image_url', ''),
        'created_at': datetime.utcnow()
    }
    
    products_collection.insert_one(product)
    return jsonify({"message": "Product created successfully"})

@app.route('/admin')
def admin():
    products = list(products_collection.find({}, {'_id': 0}))
    return render_template('admin.html', products=products)

@app.route('/admin/products', methods=['POST'])
def admin_create_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    category = request.form['category']
    stock = int(request.form['stock'])
    image_url = request.form['image_url']
    
    product = {
        'name': name,
        'description': description,
        'price': price,
        'category': category,
        'stock': stock,
        'image_url': image_url,
        'created_at': datetime.utcnow()
    }
    
    products_collection.insert_one(product)
    return jsonify({"message": "Product created successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3002)), debug=True)