import requests

API_TOKEN = "5fzqdjXdfFhupFynlu6GItXlODakIjrz"
WHAPI_URL = "https://gate.whapi.cloud/messages/text"

payload = {
    "to": "50247621409",
    "body" : "Hola desde el chatbot en Python!"
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {API_TOKEN}"
}

response = requests.post(WHAPI_URL, json=payload, headers=headers)
print(response.text)
