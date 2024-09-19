from flask import Flask, render_template, request, jsonify
import requests
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_website = request.form['company_website']
        
        webhook_url = "https://hook.us1.make.com/mqol68vq6uvurtuu1gmviced7hp0b1fl"
        payload = {
            "company_name": company_name,
            "company_website": company_website
        }
        
        try:
            logging.info(f"Sending request to webhook: {webhook_url}")
            response = requests.post(webhook_url, json=payload, timeout=180)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            if "Analysis" in data:
                return jsonify({"analysis": data["Analysis"]}), 200
            else:
                logging.error("Analysis data not found in response")
                return jsonify({"error": "Analysis data not found in response"}), 500
        except requests.exceptions.Timeout:
            logging.error("Webhook request timed out")
            return jsonify({"error": "Webhook request timed out"}), 504
        except requests.exceptions.RequestException as e:
            logging.error(f"Webhook request failed: {str(e)}")
            return jsonify({"error": f"Webhook request failed: {str(e)}"}), 500
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
