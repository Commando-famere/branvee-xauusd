# main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from app.core.mt5_manager import MT5Manager
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize MT5 Manager
mt5_manager = MT5Manager()

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "app": "Branvee Auto Pilot Server",
        "version": "1.0.0",
        "status": "running"
    })

@app.route('/api/v1/connect', methods=['POST'])
def connect_mt5():
    """Connect to MT5 account"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ('account', 'password', 'server')):
        return jsonify({"success": False, "error": "Missing credentials"}), 400
    
    session_id = str(uuid.uuid4())
    result = mt5_manager.connect(session_id, data)
    return jsonify(result)

@app.route('/api/v1/disconnect/<session_id>', methods=['POST'])
def disconnect_mt5(session_id):
    """Disconnect MT5 account"""
    result = mt5_manager.disconnect(session_id)
    return jsonify(result)

@app.route('/api/v1/account/<session_id>', methods=['GET'])
def get_account_info(session_id):
    """Get account information"""
    info = mt5_manager.get_account_info(session_id)
    if info:
        return jsonify({"success": True, "data": info})
    return jsonify({"success": False, "error": "Session not found"}), 404

@app.route('/api/v1/sessions', methods=['GET'])
def get_active_sessions():
    """Get all active sessions"""
    sessions = mt5_manager.get_active_sessions()
    return jsonify({
        "active_sessions": sessions,
        "count": len(sessions)
    })

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "mt5_initialized": mt5_manager._initialized if hasattr(mt5_manager, '_initialized') else False,
        "active_sessions": len(mt5_manager.active_sessions) if hasattr(mt5_manager, 'active_sessions') else 0,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    print("🚀 Starting Branvee Auto Pilot Server...")
    print(f"📡 Server will run on http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
