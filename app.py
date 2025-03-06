import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the verification token as a constant (Replace with your actual token)
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route("/ebay-webhook", methods=["GET"])
def ebay_webhook():
    challenge_code = request.args.get("challenge_code")
    verification_token = request.args.get("verification_token")

    # Debugging: Print incoming values
    print(f"Received verification request: challenge_code={challenge_code}, verification_token={verification_token}")

    # Validate the verification token
    if verification_token == VERIFICATION_TOKEN:
        return jsonify({"challengeResponse": challenge_code}), 200
    else:
        return jsonify({"error": "Invalid verification token"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

