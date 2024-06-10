import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
from prometheus_client import Counter, Gauge, Summary, generate_latest

app = Flask(__name__)
CORS(app)

# Metrics
REQUEST_COUNT = Counter('app_service_request_count', 'Total number of requests')
IN_PROGRESS_REQUESTS = Gauge('app_service_in_progress_requests', 'Number of in-progress requests')
REQUEST_LATENCY = Summary('app_service_request_latency_seconds', 'Request latency in seconds')

# Use environment variable or default to 'model-service:5000'
MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL", "http://model-service:5000")

def handle_prediction_request(url):
    if url:
        try:
            with IN_PROGRESS_REQUESTS.track_inprogress():
                start_time = time.time()
                response = requests.post(f"{MODEL_SERVICE_URL}/predict", json={'url': url})
                response.raise_for_status()
                REQUEST_COUNT.inc()
                REQUEST_LATENCY.observe(time.time() - start_time)
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

@app.route('/metrics')
def metrics():
    return generate_latest(), 200

# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
