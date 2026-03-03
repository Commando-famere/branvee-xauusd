from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
sessions = {}
positions = {}

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
    session_id = str(uuid.uuid4())
    
    # Store session
    sessions[session_id] = {
        "account": data.get('account'),
        "server": data.get('server'),
        "connected_at": datetime.now().isoformat(),
        "balance": 10000.50,
        "equity": 10250.75
    }
    
    return jsonify({
        "success": True,
        "session_id": session_id,
        "balance": 10000.50,
        "equity": 10250.75,
        "currency": "USD"
    })

@app.route('/api/v1/account/<session_id>', methods=['GET'])
def get_account(session_id):
    """Get account info"""
    if session_id in sessions:
        return jsonify({
            "success": True,
            "balance": sessions[session_id]['balance'],
            "equity": sessions[session_id]['equity'],
            "profit": 250.25
        })
    return jsonify({"success": False, "error": "Session not found"}), 404

@app.route('/api/v1/trade', methods=['POST'])
def place_trade():
    """Place a trade"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    if session_id not in sessions:
        return jsonify({"success": False, "error": "Session not found"}), 404
    
    trade_id = str(uuid.uuid4())[:8]
    positions[trade_id] = {
        "session_id": session_id,
        "symbol": data.get('symbol', 'EURUSD'),
        "type": data.get('type', 'BUY'),
        "volume": data.get('volume', 0.01),
        "open_price": 1.08765,
        "stop_loss": data.get('stop_loss'),
        "take_profit": data.get('take_profit'),
        "open_time": datetime.now().isoformat()
    }
    
    return jsonify({
        "success": True,
        "trade_id": trade_id,
        "open_price": 1.08765,
        "message": f"{data.get('type')} order placed successfully"
    })

@app.route('/api/v1/positions/<session_id>', methods=['GET'])
def get_positions(session_id):
    """Get all open positions"""
    open_positions = []
    for tid, pos in positions.items():
        if pos['session_id'] == session_id:
            open_positions.append({
                "trade_id": tid,
                "symbol": pos['symbol'],
                "type": pos['type'],
                "volume": pos['volume'],
                "open_price": pos['open_price'],
                "current_price": 1.08890,  # Simulated current price
                "profit": 12.50  # Simulated profit
            })
    
    return jsonify({
        "success": True,
        "positions": open_positions,
        "count": len(open_positions)
    })

@app.route('/api/v1/close/<trade_id>', methods=['POST'])
def close_trade(trade_id):
    """Close a specific trade"""
    if trade_id in positions:
        closed_trade = positions.pop(trade_id)
        return jsonify({
            "success": True,
            "trade_id": trade_id,
            "close_price": 1.08950,
            "profit": 15.75,
            "message": "Trade closed successfully"
        })
    return jsonify({"success": False, "error": "Trade not found"}), 404

if __name__ == '__main__':
    print("🚀 Branvee Auto Pilot Server Starting...")
    print("📡 Listening on http://0.0.0.0:5000")
    print("Trading endpoints enabled!")
    app.run(host='0.0.0.0', port=5000, debug=True)
