import json
import logging
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# 🔹 Enable Logging for Debugging
logging.basicConfig(level=logging.DEBUG)

# 🔹 eBay Verification Token (Replace with the actual token from eBay Developer Portal)
VERIFICATION_TOKEN = "roosty_verification_token_1234567890"

@app.route("/api/ebay-deletion", methods=["GET", "POST"])
def ebay_deletion():
    if request.method == "GET":
        # 🔹 Handle eBay's challenge request
        challenge_code = request.args.get("challenge_code")
        if challenge_code:
            endpoint = "https://roosty-api.onrender.com/api/ebay-deletion"  # Replace with your actual URL
            response_data = challenge_code + VERIFICATION_TOKEN + endpoint
            challenge_response = hashlib.sha256(response_data.encode()).hexdigest()
            return jsonify({"challengeResponse": challenge_response}), 200

    elif request.method == "POST":
        # 🔹 Log the full request body for debugging
        try:
            data = request.get_json()
            if data is None:
                logging.error("Received empty request body.")
                return jsonify({"error": "Missing JSON body"}), 400

            logging.debug(f"Received POST request: {json.dumps(data, indent=2)}")

            # 🔹 Check if `notificationEventName` is present
            event_name = data.get("notificationEventName")
            if not event_name:
                logging.error("Missing 'notificationEventName' in request.")
                return jsonify({"error": "Invalid request format: missing 'notificationEventName'"}), 400

            # 🔹 Process eBay Account Closure Request
            if event_name == "EBAY_ACCOUNT_CLOSURE":
                ebay_user_id = data.get("recipient", {}).get("username", "Unknown User")
                logging.info(f"Processing eBay account closure for user: {ebay_user_id}")

                # 🔹 Simulating deletion logic (Replace with actual database logic)
                return jsonify({"message": f"Account deletion request processed for {ebay_user_id}"}), 200

            else:
                logging.warning(f"Unsupported notification event: {event_name}")
                return jsonify({"error": "Unsupported notification event"}), 400

        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    return jsonify({"error": "Invalid request method"}), 405  # Explicitly return 405 for unsupported methods

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

