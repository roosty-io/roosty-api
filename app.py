from flask import Flask, request, jsonify

app = Flask(__name__)

# Your eBay Verification Token
VERIFICATION_TOKEN = "TYCXkCynpUtEipOOfG3EJcR1U0QarK4rAwSp2AL2URM"

@app.route('/ebay-webhook', methods=['GET', 'POST'])
def ebay_webhook():
    if request.method == 'GET':
        verification_token = request.args.get('verification_token')
        challenge = request.args.get('challenge')  # Expected challenge
        challenge_code = request.args.get('challenge_code')  # eBay's challenge_code

        # Use the correct challenge parameter
        if challenge is None:
            challenge = challenge_code  # Fallback if eBay sends challenge_code

        if verification_token == VERIFICATION_TOKEN and challenge:
            return jsonify({"challengeResponse": challenge})  # Send response

        return jsonify({"error": "Invalid verification token"}), 400

    elif request.method == 'POST':
        data = request.json
        print("🔹 Received eBay webhook:", data)
        return jsonify({"message": "Webhook received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

