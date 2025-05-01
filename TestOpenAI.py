import requests
import json

# Define the URL of your FastAPI endpoint
url = "http://localhost:8000/v1/chat/completions"

# Set the appropriate headers
headers = {
    "Content-Type": "application/json"
}

# Prepare the payload with a user message containing personal information
data = {
    "messages": [
        {
            "role": "user",
            "content": "Hallo, mein Name ist Max Moez und meine E-Mail-Adresse ist max.moez@example.com. 1. Bitte wiederhole meinen Namen genau so, wie ich ihn geschrieben habe? 2. Erzähl mir bitte einen Witz über das Wetter."
        }
    ]
}

#For testing in English
#data = {
#    "messages": [
#        {
#            "role": "user",
#            "content": "Hi, my name is Max Moez and my email is max.moez@example.com. 1.Please repeat my name back to me exactly as I wrote it? 2.A joke about weather?"
#        }
#    ]
#}

# Send the POST request to your FastAPI endpoint
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check if the response contains JSON data
try:
    response.raise_for_status()  # Raise an error for bad status codes
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
