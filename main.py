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
            response.raise_for_status()

            # Process the plain text response
            text_response = response.text
            analysis = {}
            current_key = None
            for line in text_response.split('\n'):
                line = line.strip()
                if line.startswith('**') and line.endswith('**'):
                    current_key = line.strip('**:')
                    analysis[current_key] = ""
                elif current_key and line:
                    analysis[current_key] += line + " "

            # Clean up the values
            for key in analysis:
                analysis[key] = analysis[key].strip()

            return jsonify({"analysis": analysis}), 200
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
