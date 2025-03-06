from flask import Flask, request, jsonify

app = Flask(__name__)

# Your verification token (must match what’s in eBay Developer settings)
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route("/ebay-webhook", methods=["GET"])
def verify_ebay_webhook():
    """Handles eBay webhook verification."""
    challenge_code = request.args.get("challenge_code")
    verification_token = request.args.get("verification_token")

    print(f"✅ Received verification request: challenge_code={challenge_code}, verification_token={verification_token}")

    if verification_token != VERIFICATION_TOKEN:
        print("❌ Invalid verification token received.")
        return jsonify({"error": "Invalid verification token"}), 400

    return jsonify({"challengeResponse": challenge_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

