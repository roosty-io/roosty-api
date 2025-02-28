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

    return jsonify({"message": "Authorization code received!", "code": code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
