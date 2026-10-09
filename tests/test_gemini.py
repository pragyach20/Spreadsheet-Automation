import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

model = init_chat_model(
    "gemini-3.8-flash",
    api_key=GEMINI_API_KEY,
    model_provider="google_genai"
)

response = model.invoke(
    "Summarize this customer issue in one short sentence: "
    "Rahul is unable to log in to his account and the issue has high priority."
)

print("Gemini connection successful!")
print("AI Summary:")
print(response.content)