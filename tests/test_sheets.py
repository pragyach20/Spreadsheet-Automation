import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_SPREADSHEET_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

service = build(
    "sheets",
    "v4",
    developerKey=API_KEY
)

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=SHEET_NAME
).execute()

rows = result.get("values", [])

print("Google Sheets connection successful!")
print("Rows found:")
print(rows)