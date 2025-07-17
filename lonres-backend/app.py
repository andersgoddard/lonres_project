from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime
import json
import traceback

app = Flask(__name__)
CORS(app, origins=["https://www.lonres.com"])

DATA_DIR = "/tmp/received_data"
os.makedirs(DATA_DIR, exist_ok=True)  # Create at app start

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return "Flask app is running", 200

@app.route('/receive', methods=['POST'])
def receive_data():
    import os, json
    DATA_DIR = "/tmp/received_data"
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, "all_results.json")

    if not request.is_json:
        return jsonify({"error": "Request content-type must be application/json"}), 415

    try:
        new_data = request.get_json(silent=True)
        if not new_data or "results" not in new_data:
            return jsonify({"error": "No results in JSON body"}), 400

        # Load existing results if file exists
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                existing_data = json.load(f)
        else:
            existing_data = {"results": []}

        # Append new results
        existing_data["results"].extend(new_data["results"])

        # Save combined results
        with open(filepath, "w") as f:
            json.dump(existing_data, f, indent=2)

        return jsonify({"message": "Results appended successfully"}), 200

    except Exception as e:
        logging.error("Error appending results:", exc_info=True)
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
