from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_website = request.form['company_website']
        
        # Send data to webhook
        webhook_url = "https://example.com/webhook"  # Replace with actual webhook URL
        payload = {
            "company_name": company_name,
            "company_website": company_website
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=180)  # 3 minutes timeout
            if response.status_code == 200:
                return jsonify(response.json()), 200
            else:
                return jsonify({"error": "Webhook request failed"}), 500
        except requests.exceptions.Timeout:
            return jsonify({"error": "Webhook request timed out"}), 504
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
