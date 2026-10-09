import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model

load_dotenv()

GOOGLE_SPREADSHEET_API_KEY = os.getenv("GOOGLE_SPREADSHEET_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def get_spreadsheet_data():
    """Fetch spreadsheet data"""
    service = build('sheets', 'v4', developerKey=GOOGLE_SPREADSHEET_API_KEY)
    all_rows = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=SHEET_NAME).execute()['values']
    try:
        with open('last_row.txt', encoding='utf-8') as file:
            last_row = int(file.read().strip() or '0')
    except FileNotFoundError:
        last_row = 0
        with open('last_row.txt', 'w', encoding='utf-8') as file:
            file.write('0')
    new_rows = all_rows[last_row:]
    headers = all_rows[0]
    return all_rows, new_rows, headers

def summarize_with_ai(text):
    system_prompt = """
    You are a helpful assistant that summarizes spreadsheet data.
    You will receive new rows that were added to a Google Spreadsheet.
    Please provide a clear, concise summary of this data.
    """

    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

    model = init_chat_model(
        "gemini-3.8-flash",
        api_key=GEMINI_API_KEY,
        model_provider="google_genai"
    )

    message = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Here are the new rows from the spreadsheet:\n{text}"
        }
    ]

    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Calling Gemini... Attempt {attempt}/{max_retries}")

            response = model.invoke(message).content

            if isinstance(response, list):
                response = "".join(
                    item.get("text", "")
                    for item in response
                    if isinstance(item, dict)
                )

            return str(response)

        except Exception as error:
            print(f"Gemini attempt {attempt} failed: {error}")

            if attempt < max_retries:
                import time
                print("Waiting 5 seconds before retrying...")
                time.sleep(5)
            else:
                print("Gemini failed after all retry attempts.")
                raise

def send_email(subject, body):
    """Send email with the summary."""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()
    print(f"Email sent successfully to {RECIPIENT_EMAIL}")


all_rows, new_rows, headers = get_spreadsheet_data()

if not new_rows:
    print("No new rows found. Nothing to process.")
else:
    message = f"Headers: {headers}\nNew rows: {new_rows}"
    print(message)

    summary = summarize_with_ai(message)

    body = f"Here is today's summary\n\n{summary}\n\nThanks!"

    send_email("Daily Spreadsheet Summary", body)

    # Update the last processed row only after the email is sent successfully
    total_rows = len(all_rows)
    with open("last_row.txt", "w") as file:
        file.write(str(total_rows))

    print(f"Processed {len(new_rows)} new row(s).")
    print(f"last_row.txt updated to {total_rows}.")
