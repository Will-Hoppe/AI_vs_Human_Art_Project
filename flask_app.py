import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import json
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load Firebase credentials from environment variable
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_credentials_json:
    raise ValueError("Firebase credentials not found in environment variables.")
firebase_credentials = json.loads(firebase_credentials_json)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ai-vs-human-art-project-default-rtdb.firebaseio.com/"
})

@app.route('/get-data', methods=['GET'])
def get_data():
    """Fetch data from Firebase Realtime Database."""
    ref = db.reference('/')
    data = ref.get()
    return jsonify(data), 200

@app.route('/update-data', methods=['POST'])
def update_data():
    """Update data in Firebase Realtime Database."""
    try:
        data = request.json  # JSON payload from the client
        ref = db.reference('/')
        ref.update(data)
        return jsonify({"message": "Data updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Hello, Render!"

if __name__ == "__main__":
    # Get the port from the PORT environment variable (default to 5000 if not set)
    port = int(os.getenv("PORT", 5000))
    # Bind to 0.0.0.0 to allow external connections
    app.run(host="0.0.0.0", port=port)
