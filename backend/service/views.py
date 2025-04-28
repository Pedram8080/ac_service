from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestSerializer
from kavenegar import *
from django.conf import settings
from .models import Request
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ServiceRequest
from .utils import send_sms


class CreateRequestView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "درخواست ثبت شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'home.html')


def send_request_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')

        if not name or not phone or not service_type:
            return JsonResponse({'status': 'error', 'message': 'لطفاً همه فیلدها را پر کنید.'})
        # ذخیره درخواست در دیتابیس
        service_request = ServiceRequest.objects.create(
            name=name,
            phone=phone,
            service_type='install' if service_type == 'نصب' else 'repair'
        )

        # ارسال پیامک به مشتری
        send_sms(phone, f"{name} عزیز، درخواست {service_type} شما با موفقیت ثبت شد. به زودی با شما تماس می‌گیریم.")

        # ارسال پیامک به ادمین
        admin_phone = '09352493041'  # شماره ادمین اینجا بذار
        send_sms(admin_phone, f"درخواست جدید {service_type} از {name} - {phone}")

        return JsonResponse({'status': 'success', 'message': 'درخواست شما با موفقیت ثبت شد.'})

    return JsonResponse({'status': 'error', 'message': 'متد غیرمجاز است.'})