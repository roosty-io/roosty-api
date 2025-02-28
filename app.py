import json
import logging
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# 🔹 Enable Logging for Debugging
logging.basicConfig(level=logging.DEBUG)

# 🔹 eBay Verification Token (Replace with your actual token from eBay Developer Portal)
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
        # 🔹 Log the full raw request body and headers for debugging
        try:
            raw_data = request.get_data(as_text=True)
            logging.debug(f"Received POST request raw body: {raw_data}")

            # 🔹 Try parsing JSON data
            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                logging.error("Invalid JSON received.")
                return jsonify({"error": "Invalid JSON format"}), 400

            logging.debug(f"Parsed JSON request: {json.dumps(data, indent=2)}")

            # 🔹 Extract event type from eBay's actual request format
            event_topic = data.get("metadata", {}).get("topic")
            if not event_topic:
                logging.error(f"Missing 'metadata.topic'. Full Request: {json.dumps(data, indent=2)}")
                return jsonify({"error": "Invalid request format: missing 'metadata.topic'"}), 400

            # 🔹 Process eBay Account Closure Request
            if event_topic == "MARKETPLACE_ACCOUNT_DELETION":
                ebay_user_id = data.get("notification", {}).get("data", {}).get("username", "Unknown User")
                logging.info(f"Processing eBay account closure for user: {ebay_user_id}")

                # 🔹 Simulating deletion logic (Replace with actual database logic)
                return jsonify({"message": f"Account deletion request processed for {ebay_user_id}"}), 200

            else:
                logging.warning(f"Unsupported notification event: {event_topic}")
                return jsonify({"error": "Unsupported notification event"}), 400

        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    return jsonify({"error": "Invalid request method"}), 405  # Explicitly return 405 for unsupported methods

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
