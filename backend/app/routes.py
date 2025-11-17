from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "MEDAI-Lite backend is running"}), 200