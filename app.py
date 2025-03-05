from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"message": "Webhook is running"}), 200

@app.route("/ebay-webhook", methods=["POST"])
def ebay_webhook():
    try:
        data = request.json
        print("Received Webhook Data:", data)

        # Verify the notification type
        if "notification" in data and data["notification"] == "MARKETPLACE_ACCOUNT_DELETION":
            print("Processing account deletion request...")
            return jsonify({"message": "Account deletion request received"}), 200

        return jsonify({"message": "Webhook received"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

