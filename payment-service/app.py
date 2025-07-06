from flask import Flask, render_template, request, jsonify
import pymongo
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://admin:password@localhost:27017/ecommerce_db')
client = pymongo.MongoClient(MONGODB_URI)
db = client.ecommerce_db
payments_collection = db.payments

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "payment-service"})

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = list(payments_collection.find({}, {'_id': 0}))
    return jsonify(payments)

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    
    payment = {
        'payment_id': f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'order_id': data['order_id'],
        'amount': float(data['amount']),
        'payment_method': data['payment_method'],
        'status': 'completed',
        'transaction_id': f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        'created_at': datetime.utcnow()
    }
    
    payments_collection.insert_one(payment)
    return jsonify({"message": "Payment processed successfully", "payment_id": payment['payment_id']})

@app.route('/admin')
def admin():
    payments = list(payments_collection.find({}, {'_id': 0}))
    return render_template('admin.html', payments=payments)

@app.route('/admin/payments', methods=['POST'])
def admin_create_payment():
    order_id = request.form['order_id']
    amount = float(request.form['amount'])
    payment_method = request.form['payment_method']
    
    payment = {
        'payment_id': f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'order_id': order_id,
        'amount': amount,
        'payment_method': payment_method,
        'status': 'completed',
        'transaction_id': f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        'created_at': datetime.utcnow()
    }
    
    payments_collection.insert_one(payment)
    return jsonify({"message": "Payment processed successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3004)), debug=True)