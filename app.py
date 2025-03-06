from flask import Flask, request, jsonify

app = Flask(__name__)

# Your eBay verification token
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route("/ebay-webhook", methods=["GET"])
def verify_ebay_webhook():
    """Handles eBay's webhook verification request"""
    challenge_code = request.args.get("challenge_code")
    verification_token = request.args.get("verification_token")

    print(f"Received verification request: challenge_code={challenge_code}, verification_token={verification_token}")

    # Ensure verification_token matches eBay's expected token
    if verification_token == VERIFICATION_TOKEN:
        return jsonify({"challengeResponse": challenge_code}), 200
    else:
        return jsonify({"error": "Invalid verification token"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

