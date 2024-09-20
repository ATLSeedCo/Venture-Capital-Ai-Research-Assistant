# Company Research Analyzer

This is a web application that performs AI-powered company research analysis using Flask and Vanilla JS, with webhook integration to Make.com for backend processing.

## Features

- Simple web interface for inputting company name and website
- Sends data to a Make.com webhook for AI analysis
- Displays structured research results including company overview, recent news, and investment analysis
- Email export functionality to send research results to users

## Requirements

- Python 3.7+
- Flask
- Requests
- python-dotenv
- flask-cors

## Setup

1. Clone the repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Create a .env file in the root directory with your Make.com webhook URLs:
   ```
   WEBHOOK_URL=your_research_analysis_webhook_url_here
   EMAIL_EXPORT_WEBHOOK_URL=your_email_export_webhook_url_here
   ```
4. Run the application:
   ```
   python main.py
   ```

## Important Note

This application requires two Make.com automations to function properly:

1. Research Analysis Webhook: Performs the AI analysis of the company.
2. Email Export Webhook: Handles sending the research results via email.

Users of this code will need to create their own Make.com account and set up two separate automations:

1. Research Analysis Automation:
   - Receives the webhook data (company name and website)
   - Performs the AI analysis (using their preferred AI service)
   - Returns the analysis results in the required format

2. Email Export Automation:
   - Receives the webhook data (email address and research results)
   - Sends an email with the research results to the specified address

The webhook URLs for these automations should be added to the .env file as described in the setup instructions.

## Usage

1. Access the web interface (default: http://localhost:5000)
2. Enter a company name and website
3. Click "Run Research Analysis"
4. Wait for the results to be displayed

## Email Export Feature

This application includes an email export feature that allows users to send the research results to their email address.

1. After receiving the research results, an "Export Results to Email" section will appear.
2. Enter your email address in the provided field.
3. Click the "Send" button to receive the research results via email.

Note: The email export feature uses a separate webhook from the one used for the research process.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
