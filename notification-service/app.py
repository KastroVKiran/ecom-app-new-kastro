from flask import Flask, render_template, request, jsonify
import pymongo
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://admin:password@localhost:27017/ecommerce_db')
client = pymongo.MongoClient(MONGODB_URI)
db = client.ecommerce_db
notifications_collection = db.notifications

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "notification-service"})

@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = list(notifications_collection.find({}, {'_id': 0}))
    return jsonify(notifications)

@app.route('/notifications', methods=['POST'])
def create_notification():
    data = request.get_json()
    
    notification = {
        'notification_id': f"NOT{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'user_id': data['user_id'],
        'title': data['title'],
        'message': data['message'],
        'type': data.get('type', 'info'),
        'status': 'sent',
        'created_at': datetime.utcnow()
    }
    
    notifications_collection.insert_one(notification)
    return jsonify({"message": "Notification sent successfully", "notification_id": notification['notification_id']})

@app.route('/admin')
def admin():
    notifications = list(notifications_collection.find({}, {'_id': 0}))
    return render_template('admin.html', notifications=notifications)

@app.route('/admin/notifications', methods=['POST'])
def admin_create_notification():
    user_id = request.form['user_id']
    title = request.form['title']
    message = request.form['message']
    notification_type = request.form['type']
    
    notification = {
        'notification_id': f"NOT{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'user_id': user_id,
        'title': title,
        'message': message,
        'type': notification_type,
        'status': 'sent',
        'created_at': datetime.utcnow()
    }
    
    notifications_collection.insert_one(notification)
    return jsonify({"message": "Notification sent successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3005)), debug=True)