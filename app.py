from flask import Flask, request, jsonify

app = Flask(__name__)

# Replace this with your actual verification token
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route('/ebay-webhook', methods=['GET'])
def verify_ebay_webhook():
    """Handles eBay's webhook verification request."""
    challenge_code = request.args.get("challenge_code")
    verification_token = request.args.get("verification_token")

    if verification_token != VERIFICATION_TOKEN:
        return jsonify({"error": "Invalid verification token"}), 400

    return jsonify({"challengeResponse": challenge_code}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

