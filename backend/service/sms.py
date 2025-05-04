import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

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
        
        logger.info(f"ارسال پیامک به {to} با متن: {text}")
        logger.info(f"داده‌های ارسالی: {data}")
        
        # ارسال درخواست با فرمت form-data
        response = requests.post(
            settings.SMS_API_URL,
            data=data,
            headers=headers,
            timeout=10  # اضافه کردن تایم‌اوت
        )
        
        logger.info(f"وضعیت پاسخ: {response.status_code}")
        logger.info(f"پاسخ خام: {response.text}")
        
        try:
            response_data = response.json()
            logger.info(f"پاسخ JSON: {response_data}")
            
            # بررسی وضعیت ارسال
            if response.status_code == 200:
                if isinstance(response_data, dict) and response_data.get('status') == 'ارسال شد':
                    logger.info("پیامک با موفقیت ارسال شد")
                    return True
                else:
                    logger.error(f"خطا در پاسخ API: {response_data}")
                    return False
            else:
                logger.error(f"خطای HTTP: {response.status_code}")
                return False
                
        except ValueError as e:
            logger.error(f"خطا در تبدیل پاسخ به JSON: {e}")
            logger.error(f"پاسخ خام: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"خطا در ارسال درخواست: {e}")
        return False
    except Exception as e:
        logger.error(f"خطای ناشناخته: {e}")
        return False
