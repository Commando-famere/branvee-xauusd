from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "app": "Branvee Auto Pilot Server",
        "version": "1.0.0",
        "status": "running"
    })

@app.route('/api/v1/connect', methods=['POST'])
def connect_mt5():
    """Connect to MT5 account"""
    data = request.get_json()
    
    # Simulate MT5 connection
    return jsonify({
        "success": True,
        "session_id": "test-session-123",
        "balance": 10000.50,
        "equity": 10250.75,
        "currency": "USD"
    })

@app.route('/api/v1/account/<session_id>', methods=['GET'])
def get_account(session_id):
    """Get account info"""
    return jsonify({
        "success": True,
        "balance": 10000.50,
        "equity": 10250.75,
        "profit": 250.25
    })

if __name__ == '__main__':
    print("🚀 Branvee Auto Pilot Server Starting...")
    print("📡 Listening on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
