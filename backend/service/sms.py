import requests
from django.conf import settings
import logging

logger = logging.getLogger('service.sms')

def send_sms(to, text):
    try:
        # ساختار درخواست مطابق با مستندات ملی پیامک
        data = {
            'to': to,
            'from': settings.SMS_FROM,
            'text': text
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        logger.info("="*50)
        logger.info("شروع ارسال پیامک")
        logger.info(f"URL: {settings.SMS_API_URL}")
        logger.info(f"به: {to}")
        logger.info(f"متن: {text}")
        logger.info(f"از: {settings.SMS_FROM}")
        logger.info(f"داده‌های ارسالی: {data}")
        logger.info(f"هدرها: {headers}")
        
        # ارسال درخواست
        response = requests.post(
            settings.SMS_API_URL,
            json=data,
            headers=headers,
            timeout=10
        )
        
        logger.info(f"وضعیت پاسخ: {response.status_code}")
        logger.info(f"پاسخ خام: {response.text}")
        logger.info(f"هدرهای پاسخ: {response.headers}")
        
        try:
            response_data = response.json()
            logger.info(f"پاسخ JSON: {response_data}")
            
            # بررسی وضعیت ارسال
            if response.status_code == 200:
                if isinstance(response_data, dict):
                    status = response_data.get('status', '').lower()
                    logger.info(f"وضعیت ارسال: {status}")
                    if status == 'ارسال شد':
                        logger.info("پیامک با موفقیت ارسال شد")
                        return True
                    elif status == 'ارسال نشده':
                        logger.error("پیامک ارسال نشد")
                        return False
                    else:
                        logger.error(f"وضعیت نامشخص: {status}")
                        return False
                else:
                    logger.error(f"فرمت پاسخ نامعتبر: {response_data}")
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
    finally:
        logger.info("پایان ارسال پیامک")
        logger.info("="*50)
