from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route("/ebay-webhook", methods=["GET"])
def verify():
    """Handles eBay validation requests and returns the challenge code"""
    challenge_code = request.args.get("challenge_code")

    if challenge_code:
        print(f"Received verification request: challenge_code={challenge_code}")
        return jsonify({"challengeResponse": challenge_code}), 200

    return jsonify({"error": "Missing challenge_code"}), 400

@app.route("/ebay-webhook", methods=["POST"])
def handle_notification():
    """Handles actual eBay deletion notifications"""
    data = request.json

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    verification_token = data.get("verification_token")

    if verification_token != VERIFICATION_TOKEN:
        return jsonify({"error": "Invalid verification token"}), 403

    print(f"Received deletion request: {data}")
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

