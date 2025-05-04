import requests
from django.conf import settings


def send_sms(to: str, text: str):
    url = settings.SMS_API_URL
    data = {
        'from': settings.SMS_FROM,
        'to': to,
        'text': text
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        return {'error': str(e)}
