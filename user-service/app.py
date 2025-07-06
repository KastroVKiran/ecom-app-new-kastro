from flask import Flask, render_template, request, jsonify
import pymongo
import os
from datetime import datetime
import hashlib

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://admin:password@localhost:27017/ecommerce_db')
client = pymongo.MongoClient(MONGODB_URI)
db = client.ecommerce_db
users_collection = db.users

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "user-service"})

@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Hash password
    password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
    
    user = {
        'username': data['username'],
        'email': data['email'],
        'password_hash': password_hash,
        'full_name': data['full_name'],
        'role': data.get('role', 'user'),
        'created_at': datetime.utcnow()
    }
    
    users_collection.insert_one(user)
    return jsonify({"message": "User created successfully"})

@app.route('/admin')
def admin():
    users = list(users_collection.find({}, {'_id': 0, 'password_hash': 0}))
    return render_template('admin.html', users=users)

@app.route('/admin/users', methods=['POST'])
def admin_create_user():
    username = request.form['username']
    email = request.form['email']
    full_name = request.form['full_name']
    role = request.form['role']
    password = request.form['password']
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    user = {
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'full_name': full_name,
        'role': role,
        'created_at': datetime.utcnow()
    }
    
    users_collection.insert_one(user)
    return jsonify({"message": "User created successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3001)), debug=True)