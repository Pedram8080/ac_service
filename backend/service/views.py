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
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


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

        if not re.fullmatch(r'09\d{9}', phone):
            return JsonResponse(
                {'status': 'error', 'message': 'شماره موبایل نامعتبر است. لطفاً یک شماره صحیح وارد کنید.'})

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


def request_panel_view(request):
    requests = ServiceRequest.objects.all().order_by('-id')
    return render(request, 'service/panel.html', {'requests': requests})

@csrf_exempt
@login_required
def update_status_view(request, request_id):
    if request.method == 'POST':
        try:
            req = ServiceRequest.objects.get(id=request_id)
            if req.status == 'pending':
                req.status = 'done'
                message = 'درخواست انجام شد!'
            else:
                req.status = 'pending'
                message = 'در حال بررسی'
            req.save()
            return JsonResponse({'success': True, 'message': message})
        except:
            return JsonResponse({'success': False})

