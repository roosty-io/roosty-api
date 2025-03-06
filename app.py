import hashlib
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define your verification token (Must match the eBay Developer Portal)
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

# Define your webhook endpoint URL (Must match what you submitted in eBay settings)
ENDPOINT_URL = "https://roosty-api.onrender.com/ebay-webhook"  # Make sure this is correct

@app.route("/ebay-webhook", methods=["GET"])
def verify_ebay_webhook():
    """Handles eBay webhook verification requests by responding with a hashed challengeResponse."""
    challenge_code = request.args.get("challenge_code")

    if not challenge_code:
        return jsonify({"error": "Missing challenge_code"}), 400

    # Compute the SHA-256 hash: challenge_code + verification_token + endpoint
    hash_input = f"{challenge_code}{VERIFICATION_TOKEN}{ENDPOINT_URL}".encode("utf-8")
    challenge_response = hashlib.sha256(hash_input).hexdigest()

    print(f"✅ Received verification request: challenge_code={challenge_code}")
    print(f"🔹 Computed challengeResponse: {challenge_response}")

    return jsonify({"challengeResponse": challenge_response})

@app.route("/ebay-webhook", methods=["POST"])
def handle_ebay_notification():
    """Handles incoming eBay marketplace account deletion notifications."""
    try:
        data = request.json
        print("🔔 Received eBay Deletion Notification:", json.dumps(data, indent=2))

        # Check if the notification is about a marketplace account deletion
        if "notification" in data and data["notification"].get("topic") == "MARKETPLACE_ACCOUNT_DELETION":
            deleted_user = data["notification"]["payload"].get("userId", "Unknown User")
            print(f"🚨 eBay account deleted: {deleted_user}")

            # Acknowledge receipt of the notification
            return jsonify({"status": "received"}), 200
        else:
            print("⚠️ Unknown notification received.")
            return jsonify({"error": "Invalid notification format"}), 400
    except Exception as e:
        print(f"❌ Error processing eBay notification: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

