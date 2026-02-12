import requests
from django.conf import settings

def send_email_via_api():

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "Vishal",
            "email": "kumarraj741736@gmail.com"
        },
        "to": [
            {
                "email": "rajthakurparihar74@gmail.com",
                "name": "Raj"
            }
        ],
        "subject": "Test via API",
        "htmlContent": "<h1>Email working via Brevo API</h1>"
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.text)