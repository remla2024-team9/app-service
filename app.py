import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

MODEL_SERVICE_URL = "127.0.0.1:5000"


def handle_prediction_request(url):
    if url:
        response = requests.post(f"http://{MODEL_SERVICE_URL}/predict", json={'url': url})
        return jsonify(response.json()), response.status_code
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
