# Company Research Analyzer

This is a web application that performs AI-powered company research analysis using Flask and Vanilla JS, with webhook integration to Make.com for backend processing.

## Features

- Simple web interface for inputting company name and website
- Sends data to a Make.com webhook for AI analysis
- Displays structured research results including company overview, recent news, and investment analysis

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
3. Create a .env file in the root directory with your Make.com webhook URL:
   ```
   WEBHOOK_URL=your_make_com_webhook_url_here
   ```
4. Run the application:
   ```
   python main.py
   ```

## Important Note

This application requires a Make.com automation to function properly. Users of this code will need to create their own Make.com account and set up an automation that:

1. Receives the webhook data (company name and website)
2. Performs the AI analysis (using their preferred AI service)
3. Returns the analysis results in the required format

The webhook URL for this automation should be added to the .env file as described in the setup instructions.

## Usage

1. Access the web interface (default: http://localhost:5000)
2. Enter a company name and website
3. Click "Run Research Analysis"
4. Wait for the results to be displayed

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check issues page if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)
