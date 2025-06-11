import requests
import json

# Define the URL of your FastAPI endpoint
url = "http://localhost:8000/v1/chat/completions"

# Set the appropriate headers
headers = {
    "Content-Type": "application/json"
}

# Payload with a famous person's name
data = {
    "messages": [
        {
            "role": "user",
            "content": "Hallo, ich habe einen Artikel über Angela Merkel geschrieben. Kannst du mir bitte sagen, was ihre Rolle in der deutschen Politik war?"
        }
    ]
}

# Optional: English version
# data = {
#     "messages": [
#         {
#             "role": "user",
#             "content": "Hi, I want to learn about Friedrich Merz. Can you summarize his political career?"
#         }
#     ]
# }

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Handle response
try:
    response.raise_for_status()
    json_response = response.json()
    print(json.dumps(json_response, indent=2))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except json.JSONDecodeError as json_err:
    print(f"JSON decode error: {json_err}")
    print(f"Response content: {response.text}")
except Exception as err:
    print(f"An error occurred: {err}")
    print(f"Response content: {response.text}")
