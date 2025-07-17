from flask import Flask, request, jsonify
import logging
import os
from datetime import datetime
import json
import traceback

app = Flask(__name__)

DATA_DIR = "/tmp/received_data"
os.makedirs(DATA_DIR, exist_ok=True)  # Create at app start

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return "Flask app is running", 200

@app.route('/receive', methods=['POST'])
def receive_data():
    if not request.is_json:
        return jsonify({"error": "Request content-type must be application/json"}), 415

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Empty or invalid JSON body"}), 400

        os.makedirs(DATA_DIR, exist_ok=True)  # ✅ Ensure the directory exists

        filename = datetime.now().strftime("%Y%m%d_%H%M%S.json")
        filepath = os.path.join(DATA_DIR, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        logging.info(f"✅ Data received and saved to {filepath}")
        return jsonify({"message": "Data received successfully"}), 200

    except Exception as e:
        logging.error("Error processing request:")
        logging.error(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

@app.route('/latest', methods=['GET'])
def get_latest_data():
    try:
        os.makedirs(DATA_DIR, exist_ok=True)

        json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
        if not json_files:
            return jsonify({"message": "No data files found"}), 404
        
        # Sort by newest first
        json_files.sort(reverse=True)
        latest_file = os.path.join(DATA_DIR, json_files[0])

        with open(latest_file, 'r') as f:
            contents = json.load(f)

        return jsonify({
            "filename": json_files[0],
            "data": contents
        })

    except Exception as e:
        logging.error("Error reading latest file:", exc_info=True)
        return jsonify({"error": "Failed to read latest data file"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
