import requests
import json

url = "http://localhost:8000/analyze"
headers = {"Content-Type": "application/json"}

#Testing German
data = {
    "text": "Hallo, mein Name ist Max Mustermann. Meine E-Mail-Adresse ist max.mustermann@example.de und meine Telefonnummer ist +49 123 4567890."
}

#Testing English
#data = {
#    "text": "Hello, my name is John Doe. My email is john.doe@example.com and my phone number is +49 123 4567890."
#}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
