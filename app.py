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

    elif request.method == "POST":
        # Handle actual account deletion requests
        data = request.get_json()
        if data and data.get("notificationEventName") == "EBAY_ACCOUNT_CLOSURE":
            ebay_user_id = data.get("recipient", {}).get("username")
            print(f"Received eBay account closure request for user: {ebay_user_id}")
            return jsonify({"message": "Account deletion request received"}), 200

    return jsonify({"error": "Invalid request"}), 405  # Return correct error for unsupported methods

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
