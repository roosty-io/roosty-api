import hashlib
import json
import os
from flask import Flask, request, jsonify
from supabase import create_client

app = Flask(__name__)

# eBay Webhook Configuration
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"
ENDPOINT_URL = "https://roosty-api.onrender.com/ebay-webhook"

# Supabase Configuration
SUPABASE_URL = "https://your-supabase-url.supabase.co"
SUPABASE_KEY = "your-supabase-api-key"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/ebay-webhook", methods=["GET"])
def verify_ebay_webhook():
    """Handles eBay webhook verification requests."""
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

        # ✅ Fix: Correctly check event type
        event_type = data.get("metadata", {}).get("topic")
        if event_type != "MARKETPLACE_ACCOUNT_DELETION":
            print("⚠️ Invalid notification type received:", event_type)
            return jsonify({"error": "Invalid notification type"}), 400

        # ✅ Fix: Correctly extract userId
        deleted_user = data.get("notification", {}).get("data", {}).get("userId")
        if not deleted_user:
            print("❌ Missing user ID in deletion event.")
            return jsonify({"error": "Missing user ID"}), 400

        print(f"🚨 eBay account deleted: {deleted_user}")

        # ✅ Remove user from Supabase database
        response = supabase.table("users").delete().match({"ebay_user_id": deleted_user}).execute()

        if response.data:
            print(f"✅ Successfully deleted user: {deleted_user}")
            return jsonify({"status": "User deleted successfully"}), 200
        else:
            print(f"❌ Error deleting user {deleted_user}: {response.error}")
            return jsonify({"error": "Failed to delete user"}), 500

    except Exception as e:
        print(f"❌ Error processing eBay notification: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

