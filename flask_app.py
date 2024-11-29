import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
import json

# Initialize Flask app
app = Flask(__name__)

# Load Firebase credentials from environment variable
firebase_credentials_json = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_credentials_json:
    raise ValueError("Firebase credentials not found in environment variables.")
firebase_credentials = json.loads(firebase_credentials_json)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://<your-database-name>.firebaseio.com/"
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

if __name__ == '__main__':
    app.run(debug=True)
