from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestSerializer
from kavenegar import *
from django.conf import settings
from .models import Request
import requests
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import ServiceRequest
from .sms import send_sms
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from service.sms import send_sms  # مسیر رو بر اساس پروژه خودت اصلاح کن


class CreateRequestView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "درخواست ثبت شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'home.html')


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


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow:",
        "Sitemap: https://nasbfix.ir/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def article_view(request):
    return render(request, 'article.html')


@csrf_protect
def request_specialist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')

        # ایجاد درخواست جدید با مدل ServiceRequest
        ServiceRequest.objects.create(
            name=name,
            phone=phone,
            service_type=service_type,
            status='pending'
        )

        # ارسال پیامک به مشتری
        customer_message = f'{name} عزیز، درخواست شما برای {service_type} ثبت شد. با تشکر از شما.'
        customer_data = {
            'from': settings.SMS_FROM,
            'to': phone,
            'text': customer_message
        }
        try:
            requests.post(settings.SMS_API_URL, json=customer_data)
        except Exception as e:
            print(f"Error sending SMS to customer: {e}")

        # ارسال پیامک به ادمین
        admin_message = f'درخواست جدید از طرف {name} - شماره: {phone} - نوع سرویس: {service_type}'
        admin_data = {
            'from': settings.SMS_FROM,
            'to': '09220760633',  # شماره مدیر
            'text': admin_message
        }
        try:
            requests.post(settings.SMS_API_URL, json=admin_data)
        except Exception as e:
            print(f"Error sending SMS to admin: {e}")

        return JsonResponse({
            'status': 'success',
            'message': 'درخواست شما با موفقیت ثبت شد'
        })

    return JsonResponse({
        'status': 'error',
        'message': 'متد درخواست نامعتبر است'
    }, status=400)