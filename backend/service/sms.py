import requests
from django.conf import settings


def send_sms(to, text):
    try:
        data = {
            'to': to,
            'from': settings.SMS_FROM,
            'text': text,
            'apiKey': settings.SMS_API_KEY
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(
            settings.SMS_API_URL,
            json=data,
            headers=headers
        )
        
        print(f"پاسخ خام API پیامک: {response.text}")
        response_data = response.json()
        print(f"پاسخ JSON API پیامک: {response_data}")
        
        if response.status_code == 200 and response_data.get('status') == 'ارسال شد':
            print("پیامک با موفقیت ارسال شد")
            return True
        else:
            print(f"خطا در ارسال پیامک: {response_data}")
            return False
            
    except Exception as e:
        print(f"خطا در ارسال پیامک: {e}")
        return False
