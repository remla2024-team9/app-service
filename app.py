import os
import requests
from flask import Flask, jsonify, request   
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Use environment variable or default to 'model-service:5000'
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model-service:5000")


def handle_prediction_request(url):
    if url:
        try:
            response = requests.post(f"{MODEL_SERVICE_URL}/predict", json={'url': url})
            response.raise_for_status()
            return jsonify(response.json()), response.status_code
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request to model service failed: {e}")
            return jsonify({"error": "Failed to process request to model service"}), 500
    else:
        return jsonify({"error": "URL not provided in request"}), 400


@app.route("/submit_input", methods=['POST'])
def submit_review():
    data = request.get_json()
    review_url = data.get('input')  # Assuming 'input' contains the URL to be processed
    if review_url:
        return handle_prediction_request(review_url)
    else:
        return jsonify({"message": "No input provided"}), 400


@app.route("/send_predict_request", methods=['POST'])
def send_predict_request():
    data = request.get_json()
    url = data.get('url')
    return handle_prediction_request(url)


# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
