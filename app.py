import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/ebay-deletion", methods=["POST"])
def ebay_deletion():
    data = request.get_json()

    # Ensure this is an account deletion request
    if data.get("notificationEventName") == "EBAY_ACCOUNT_CLOSURE":
        ebay_user_id = data.get("recipient", {}).get("username")

        print(f"Received eBay account closure request for user: {ebay_user_id}")
        
        # Simulating deletion logic (you would delete data from your database here)
        
        return jsonify({"message": "Account deletion request received"}), 200

    return jsonify({"error": "Invalid request"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
