import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECIPIENT_EMAIL
msg["Subject"] = "Spreadsheet Automation - Test Email"

body = """Hello!

This is a test email from my Spreadsheet Automation project.

Gmail SMTP connection is working successfully.

Regards,
Pragya
"""

msg.attach(MIMEText(body, "plain"))

server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SENDER_EMAIL, SENDER_PASSWORD)
server.send_message(msg)
server.quit()

print("Gmail connection successful!")
print(f"Test email sent to {RECIPIENT_EMAIL}")