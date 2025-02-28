import os
import requests
import logging
from flask import Flask, request, jsonify, redirect

app = Flask(__name__)

# 🔹 Replace with your eBay Developer Credentials
EBAY_CLIENT_ID = "YOUR_CLIENT_ID"
EBAY_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
EBAY_RU_NAME = "YOUR_RU_NAME"  # eBay Redirect URL Name (RuName)

# 🔹 eBay OAuth Token URL
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# 🔹 Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)


# ✅ eBay OAuth Callback - Handles Authentication
@app.route("/oauth/callback", methods=["GET"])
def ebay_oauth_callback():
    # 🔹 Log the full callback URL for debugging
    full_url = request.url
    logging.info(f"Full OAuth Callback URL: {full_url}")

    # 🔹 Extract the authorization code from eBay's callback
    code = request.args.get("code")
    if not code:
        logging.error("Missing authorization code from eBay.")
        return jsonify({"error": "Missing authorization code"}), 400

    # 🔹 Exchange authorization code for access token
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {requests.auth._basic_auth_str(EBAY_CLIENT_ID, EBAY_CLIENT_SECRET)}"
    }
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": EBAY_RU_NAME
    }

    response = requests.post(TOKEN_URL, headers=headers, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        expires_in = token_data.get("expires_in")

        logging.info(f"Access Token: {access_token}")
        logging.info(f"Refresh Token: {refresh_token}")

        # 🔹 Redirect to success page with token info
        return redirect(f"https://roosty.io/oauth/success?ebaytkn={access_token}&tknexp={expires_in}")

    else:
        logging.error(f"OAuth Token Exchange Failed: {response.text}")
        return jsonify({"error": "OAuth token exchange failed", "details": response.text}), response.status_code


# ✅ eBay Marketplace Account Deletion Notification Endpoint
@app.route("/api/ebay-deletion", methods=["GET", "POST"])
def ebay_deletion():
    if request.method == "GET":
        return jsonify({"message": "eBay Deletion Endpoint is active"}), 200

    elif request.method == "POST":
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing JSON body"}), 400

            event_topic = data.get("metadata", {}).get("topic")
            if not event_topic:
                return jsonify({"error": "Invalid request format: missing 'metadata.topic'"}), 400

            if event_topic == "MARKETPLACE_ACCOUNT_DELETION":
                ebay_user_id = data.get("notification", {}).get("data", {}).get("username", "Unknown User")
                logging.info(f"Processing eBay account closure for user: {ebay_user_id}")

                return jsonify({"message": f"Account deletion request processed for {ebay_user_id}"}), 200

            else:
                logging.warning(f"Unsupported notification event: {event_topic}")
                return jsonify({"error": "Unsupported notification event"}), 400

        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500

    return jsonify({"error": "Invalid request method"}), 405  # Explicitly return 405 for unsupported methods


# ✅ Fix Render Port Issue - Ensure Flask Uses Render's Assigned Port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's PORT variable if available
    app.run(host="0.0.0.0", port=port)
