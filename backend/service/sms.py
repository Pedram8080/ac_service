import requests
from django.conf import settings


def send_sms(to, text):
    try:
        # ساختار درخواست مطابق با مستندات ملی پیامک
        data = {
            'username': settings.SMS_FROM,  # شماره پنل
            'password': settings.SMS_API_KEY,  # رمز عبور پنل
            'to': to,
            'from': settings.SMS_FROM,
            'text': text
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        # ارسال درخواست با فرمت form-data
        response = requests.post(
            settings.SMS_API_URL,
            data=data,
            headers=headers
        )
        
        print(f"پاسخ خام API پیامک: {response.text}")
        response_data = response.json()
        print(f"پاسخ JSON API پیامک: {response_data}")
        
        # بررسی وضعیت ارسال
        if response.status_code == 200 and response_data.get('status') == 'ارسال شد':
            print("پیامک با موفقیت ارسال شد")
            return True
        else:
            print(f"خطا در ارسال پیامک: {response_data}")
            return False
            
    except Exception as e:
        print(f"خطا در ارسال پیامک: {e}")
        return False
