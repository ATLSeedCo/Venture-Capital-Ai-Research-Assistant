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
            logging.info(f"Sending request to webhook for company: {company_name}")
            response = requests.post(webhook_url, json=payload, timeout=180)
            response.raise_for_status()
            logging.info(f"Received response from webhook: {response.status_code}")
            
            logging.debug(f"Response content: {response.text}")

            try:
                data = response.json()
                logging.info("Successfully parsed JSON response")
                return data, 200
            except ValueError:
                logging.error("Failed to parse JSON from webhook response")
                return jsonify({"error": "Invalid response from analysis service"}), 500

        except requests.exceptions.Timeout:
            logging.error("Webhook request timed out")
            return jsonify({"error": "The request to our analysis service timed out. Please try again later."}), 504
        except requests.exceptions.RequestException as e:
            logging.error(f"Webhook request failed: {str(e)}")
            return jsonify({"error": f"There was an error connecting to our analysis service: {str(e)}"}), 500
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
    return render_template('index.html')

@app.route('/export_email', methods=['POST'])
def export_email():
    email = request.form['email']
    research_data = request.form['research_data']
    company_name = request.form['company_name']
    
    email_export_webhook_url = os.getenv('EMAIL_EXPORT_WEBHOOK_URL')
    payload = {
        "email": email,
        "research_data": research_data,
        "company_name": company_name
    }
    
    try:
        logging.info(f"Sending email export request for email: {email}")
        response = requests.post(email_export_webhook_url, json=payload, timeout=60)
        response.raise_for_status()
        logging.info(f"Received response from email export webhook: {response.status_code}")
        
        response_html = response.text.strip()
        return jsonify({"message": response_html, "content_type": "html"}), 200
    except requests.exceptions.RequestException as e:
        logging.error(f"Email export webhook request failed: {str(e)}")
        response_text = e.response.text if hasattr(e, 'response') and e.response is not None else str(e)
        return jsonify({"error": f"There was an error sending the email export request: {response_text}", "content_type": "text"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
