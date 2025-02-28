import json
import logging
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# 🔹 Enable Logging for Debugging
logging.basicConfig(level=logging.DEBUG)

# 🔹 eBay Verification Token (Replace with the actual token from eBay Developer Portal)
VERIFICATION_TOKEN = "roosty_verification_token_1234567890"

@app.route("/api/ebay-deletion", methods=["GET", "POST"])
def ebay_deletion():
    if request.method == "GET":
        # 🔹 Handle eBay's challenge request
        challenge_code = request.args.get("challenge_code")
        if challenge_code:
            endpoint = "https://roosty-api.onrender.com/api/ebay-deletion"  # Replace with your actual URL
            response_data = challenge_code + VERIFICATION_TOKEN + endpoint
            challenge_response = hashlib.sha256(response_data.encode()).hexdigest()
            return jsonify({"challengeResponse": challenge_response}), 200

    elif request.method == "POST":
        # 🔹 Log the full request body for debugging
        try:
            data = request.get_json()
            logging.debug(f"Received POST request: {json.dumps(data, indent=2)}")

            # 🔹 Validate that JSON data exists
  
