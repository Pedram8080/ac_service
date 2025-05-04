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

        # پیام به کاربر
        user_text = f"{name} عزیز، درخواست شما برای سرویس {service_type} با موفقیت ثبت شد. در اسرع وقت با شما تماس می‌گیریم."
        send_sms(phone, user_text)

        # پیام به ادمین
        admin_text = f"درخواست جدید:\nنام: {name}\nشماره: {phone}\nنوع سرویس: {service_type}"
        send_sms('09220760633', admin_text)  # شماره ادمین رو جایگزین کن

        return HttpResponse("درخواست با موفقیت ثبت شد.")

    return render(request, 'home.html')  # اسم قالب رو بذار جای your_template.html