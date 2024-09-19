import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_website = request.form['company_website']
        
        webhook_url = os.getenv('WEBHOOK_URL')
        payload = {
            "company_name": company_name,
            "company_website": company_website
        }
        
        try:
            logging.info(f"Sending request to webhook")
            response = requests.post(webhook_url, json=payload, timeout=180)
            response.raise_for_status()

            # Directly return the JSON response from the webhook
            return response.json(), 200
        except requests.exceptions.Timeout:
            logging.error("Webhook request timed out")
            return jsonify({"error": "The request to our analysis service timed out. Please try again later."}), 504
        except requests.exceptions.RequestException as e:
            logging.error(f"Webhook request failed: {str(e)}")
            return jsonify({"error": "There was an error connecting to our analysis service. Please try again later."}), 500
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": "An unexpected error occurred. Our team has been notified."}), 500
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
