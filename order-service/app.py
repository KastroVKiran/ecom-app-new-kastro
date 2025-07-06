from flask import Flask, render_template, request, jsonify
import pymongo
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://admin:password@localhost:27017/ecommerce_db')
client = pymongo.MongoClient(MONGODB_URI)
db = client.ecommerce_db
orders_collection = db.orders

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "order-service"})

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = list(orders_collection.find({}, {'_id': 0}))
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    order = {
        'order_id': f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'user_id': data['user_id'],
        'items': data['items'],
        'total_amount': float(data['total_amount']),
        'status': 'pending',
        'shipping_address': data['shipping_address'],
        'created_at': datetime.utcnow()
    }
    
    orders_collection.insert_one(order)
    return jsonify({"message": "Order created successfully", "order_id": order['order_id']})

@app.route('/admin')
def admin():
    orders = list(orders_collection.find({}, {'_id': 0}))
    return render_template('admin.html', orders=orders)

@app.route('/admin/orders', methods=['POST'])
def admin_create_order():
    user_id = request.form['user_id']
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    total_amount = quantity * price
    shipping_address = request.form['shipping_address']
    
    order = {
        'order_id': f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'user_id': user_id,
        'items': [{'product_name': product_name, 'quantity': quantity, 'price': price}],
        'total_amount': total_amount,
        'status': 'pending',
        'shipping_address': shipping_address,
        'created_at': datetime.utcnow()
    }
    
    orders_collection.insert_one(order)
    return jsonify({"message": "Order created successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3003)), debug=True)