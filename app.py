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
        # Handle actual account deletion notifications
        try:
            data = request.get_json()

            # Check if the request contains valid data
            if not data:
                return jsonify({"error": "Missing JSON body"}), 400
            
            if "notificationEventName" not in data:
                return jsonify({"error": "Invalid request format: missing 'notificationEventName'"}), 400

            if data["notificationEventName"] == "EBAY_ACCOUNT_CLOSURE":
                ebay_user_id = data.get("recipient", {}).get("username", "Unknown User")
                print(f"Received eBay account closure request for user: {ebay_user_id}")

                # Simulating deletion logic (Replace with actual database deletion)
                return jsonify({"message": "Account deletion request processed"}), 200

            else:
                return jsonify({"error": "Invalid event type"}), 400

        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    return jsonify({"error": "Invalid request method"}), 405  # Explicitly return 405 for unsupported methods

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
