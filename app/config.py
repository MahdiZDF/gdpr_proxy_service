from dotenv import load_dotenv
import os

load_dotenv()  # This will load variables from the .env file into the environment

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
