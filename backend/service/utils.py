import requests
from django.conf import settings

def send_sms(to, text):
    """
    Send SMS using MeliPayamak API
    """
    url = "https://console.melipayamak.com/api/send/simple/00cbcb3c6819459d942f96c2943fa3e3"
    
    payload = {
        "from": "50002710093341",
        "to": to,
        "text": text
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True, "پیامک با موفقیت ارسال شد"
    except requests.exceptions.RequestException as e:
        return False, f"خطا در ارسال پیامک: {str(e)}" 