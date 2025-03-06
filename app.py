from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Set your eBay verification token (must match what you entered in eBay Developer Portal)
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"
WEBHOOK_ENDPOINT = "https://roosty-api.onrender.com/ebay-webhook"  # Your actual Render webhook URL

@app.route("/ebay-webhook", methods=["GET", "POST"])
def ebay_webhook():
    if request.method == "GET":
        # eBay validation request
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            return jsonify({"error": "Missing challenge_code"}), 400

        # Hashing as per eBay's requirements: challengeCode + verificationToken + endpoint URL
        hash_string = challenge_code + VERIFICATION_TOKEN + WEBHOOK_ENDPOINT
        challenge_response = hashlib.sha256(hash_string.encode()).hexdigest()

        print(f"✅ Received verification request: challenge_code={challenge_code}")
        return jsonify({"challengeResponse": challenge_response}), 200

    elif request.method == "POST":
        # Handle eBay account deletion notification
        try:
            data = request.json
            print("🔔 Received eBay Deletion Notification:", data)

            # Check if the notification is about account deletion
            if isinstance(data, dict) and "notification" in data:
                notification = data["notification"]
                if notification.get("topic") == "MARKETPLACE_ACCOUNT_DELETION":
                    deleted_user = notification.get("payload", {}).get("userId", "Unknown User")
                    print(f"🚨 eBay account deleted: {deleted_user}")
                    return jsonify({"status": "received"}), 200
                else:
                    print("❌ Invalid notification type received")
                    return jsonify({"error": "Invalid notification type"}), 400
            else:
                print("❌ Malformed eBay notification payload")
                return jsonify({"error": "Malformed request"}), 400

        except Exception as e:
            print(f"❌ Error processing eBay notification: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

