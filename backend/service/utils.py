from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings


def send_sms(receptor, message):
    try:
        api = KavenegarAPI('35616E6438374D4354352F66624F4B544E61552B6A30756E795958695A464454386F4E696A746D71624D4D3D')
        params = {
            'sender': '2000660110',  # خط ارسال‌کننده
            'receptor': receptor,
            'message': message
        }
        response = api.sms_send(params)
        return response
    except (APIException, HTTPException) as e:
        print("SMS Error:", e)
        return None
