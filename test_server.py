from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "app": "Branvee Auto Pilot Server",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/api/v1/connect', methods=['POST'])
def connect():
    data = request.get_json()
    return jsonify({
        "success": True,
        "session_id": "test-session-123",
        "balance": 10000,
        "equity": 10250
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
