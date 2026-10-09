# AI-Powered Spreadsheet Automation

A Python automation project that monitors Google Sheets for newly added records, uses Google Gemini to generate concise AI-powered summaries, and emails the summaries through Gmail SMTP.

## Features

- Fetch spreadsheet data using the Google Sheets API
- Detect newly added rows using a local processing tracker
- Summarize new records with Google Gemini
- Send summaries through Gmail SMTP
- Handle temporary Gemini API failures
- Avoid sending an email when no new rows are found
- Update the processing tracker only after email delivery succeeds
- Load credentials and configuration from environment variables

## Project Workflow

1. Read records from Google Sheets.
2. Identify rows that have not been processed.
3. Send the new records to Google Gemini.
4. Generate a concise summary.
5. Email the summary through Gmail SMTP.
6. Update the local row counter after the email is sent successfully.

## Tech Stack

- Python
- Google Sheets API
- Google Gemini API
- LangChain
- Gmail SMTP
- Google API Python Client
- python-dotenv

## Project Structure

```text
Spreadsheet_Automation/
|-- .env.example
|-- .gitignore
|-- README.md
|-- main.py
|-- email_code.py
|-- requirements.txt
`-- tests/
    |-- test_email.py
    |-- test_gemini.py
    `-- test_sheets.py
The local `.env` file and `last_row.txt` processing state are excluded from GitHub.

## Prerequisites

- Python 3
- A Google Cloud project with Google Sheets API enabled
- A Google Sheets API key
- A Gemini API key
- A Gmail account configured for SMTP using an app password, where required

## Setup

1. Install dependencies:

   `py -m pip install -r requirements.txt`

2. Copy `.env.example` to `.env`.

3. Fill in your real values in the local `.env` file:

   `GOOGLE_SPREADSHEET_API_KEY=your_google_sheets_api_key`

   `SPREADSHEET_ID=your_spreadsheet_id`

   `SHEET_NAME=your_sheet_name`

   `GEMINI_API_KEY=your_gemini_api_key`

   `SENDER_EMAIL=your_sender_email`

   `SENDER_PASSWORD=your_gmail_app_password`

   `RECIPIENT_EMAIL=your_recipient_email`

4. Run the automation:

   `py main.py`

Configure and verify the spreadsheet and email settings before running it.

## Tests

The `tests/` directory contains email, Gemini, and Google Sheets test scripts. Review their configuration before running them, as they may contact external services.

## Security

Never commit your real `.env` file, API keys, Gmail app password, or private spreadsheet data. The `.gitignore` file excludes local configuration, Python cache files, and the row-processing tracker.

## Author

Pragya Chaudhary
