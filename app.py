from flask import Flask, request, jsonify

app = Flask(__name__)

# eBay Verification Token
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route("/ebay-webhook", methods=["GET", "POST"])
def ebay_webhook():
    if request.method == "GET":
        # Handle eBay verification challenge
        verification_token = request.args.get("verification_token")
        challenge = request.args.get("challenge")

        if verification_token == VERIFICATION_TOKEN and challenge:
            return jsonify({"challengeResponse": challenge})

        return jsonify({"error": "Invalid verification token"}), 403

    elif request.method == "POST":
        # Handle actual webhook events (log them for now)
        data = request.json
        print("Received webhook data:", data)
        return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

