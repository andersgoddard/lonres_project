from flask import Flask, request, jsonify
import logging
import os
from datetime import datetime
import json
import traceback

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Directory to store received data
DATA_DIR = "received_data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route('/')
def home():
    return "Flask app is running", 200

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.json")
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logging.info(f"Data received and saved to {filepath}")
        return jsonify({"message": "Data received successfully"}), 200
    except Exception as e:
        logging.error("Error processing request:")
        logging.error(traceback.format_exc())  # ✅ Full traceback
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

