import requests
import json

# Name to expect (should not be redacted) i.e. Germany's public figures name
expected_name = "Friedrich Merz"


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
            "content": f"Hallo, ich habe einen Artikel über {expected_name} geschrieben. Kannst du mir bitte sagen, was ihre Rolle in der deutschen Politik war?"
        }
    ]
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Handle response
try:
    response.raise_for_status()
    json_response = response.json()
    response_text = json_response["choices"][0]["message"]["content"]
    print(json.dumps(json_response, indent=2))

    # Check if expected name is still there
    if expected_name in response_text:
        print(f"Success: '{expected_name}' was not redacted.")
    else:
        print(f"FAIL: '{expected_name}' was redacted or missing.")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
except json.JSONDecodeError as json_err:
    print(f"JSON decode error: {json_err}")
    print(f"Response content: {response.text}")
except Exception as err:
    print(f"An error occurred: {err}")
    print(f"Response content: {response.text}")
