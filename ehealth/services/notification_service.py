import os
import requests

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"


def send_email_notification(to_email, subject, message):
    if not SENDGRID_API_KEY:
        raise ValueError("SendGrid API key not found")

    headers = {
        "Authorization": f"Bearer {SENDGRID_API_KEY}",
        "Content-Type": "application/json"
    }

    email_data = {
        "personalizations": [{
            "to": [{"email": to_email}],
            "subject": subject
        }],
        "from": {"email": FROM_EMAIL},
        "content": [{
            "type": "text/plain",
            "value": message
        }]
    }

    response = requests.post(SENDGRID_URL, headers=headers, json=email_data)

    return response.status_code, response.text


