import json
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# 🔹 Use the SAME verification token you entered in eBay Developer Portal
VERIFICATION_TOKEN = "roosty_verification_token_1234567890"

@app.route("/api/ebay-deletion", methods=["GET", "POST"])
def ebay_deletion():
    if request.method == "GET":
        # eBay sends a challenge request for verification
        challenge_code = request.args.get("challenge_code")
        if challenge_code:
            # Compute the challenge response
            endpoint = "https://roosty-api.onrender.com/api/ebay-deletion"  # Replace with your actual URL
            response_data = challenge_code + VERIFICATION_TOKEN + endpoint
            challenge_response = hashlib.sha256(response_data.encode()).hexdigest()
            return jsonify({"challengeResponse": challenge_response}), 200

    elif request.method =
