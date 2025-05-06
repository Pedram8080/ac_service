import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ServiceRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RequestSerializer
from django.conf import settings
from .models import Request
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import ServiceRequest
import re
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
import json
from .models import Article
from .utils import send_sms

logger = logging.getLogger('service.views')


class CreateRequestView(APIView):
    def post(self, request):
        serializer = RequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "درخواست ثبت شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    return render(request, 'home.html')


@login_required
def request_panel_view(request):
    try:
        requests = ServiceRequest.objects.all().order_by('-id')
        print(f"تعداد درخواست‌ها در پنل: {requests.count()}")  # لاگ برای دیباگ
        return render(request, 'service/panel.html', {'requests': requests})
    except Exception as e:
        print(f"خطا در نمایش پنل: {e}")  # لاگ برای دیباگ
        return render(request, 'service/panel.html', {'requests': []})


@csrf_exempt
@login_required
def update_status_view(request, request_id):
    if request.method == 'POST':
        try:
            req = ServiceRequest.objects.get(id=request_id)
            if req.status == 'pending':
                req.status = 'done'
                message = 'درخواست انجام شد!'
                # ارسال پیامک به کاربر
                user_message = f"سلام {req.name} عزیز\nدرخواست {req.service_type} شما با موفقیت انجام شد. از اعتماد شما متشکریم."
                send_sms(req.phone, user_message)
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
    articles = Article.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'article.html', {'articles': articles})


@csrf_exempt
@require_POST
def request_specialist(request):
    try:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')

        logger.info(f"دریافت درخواست جدید: {name}, {phone}, {service_type}")

        # ذخیره درخواست
        service_request = ServiceRequest.objects.create(
            name=name,
            phone=phone,
            service_type=service_type
        )

        logger.info(f"درخواست با موفقیت ذخیره شد. ID: {service_request.id}")

        # ارسال پیامک به کاربر
        user_message = f"سلام {name} عزیز\nدرخواست {service_type} شما با موفقیت ثبت شد. به زودی با شما تماس خواهیم گرفت."
        send_sms(phone, user_message)

        # ارسال پیامک به ادمین
        admin_message = f"درخواست جدید:\nنام: {name}\nشماره: {phone}\nنوع سرویس: {service_type}"
        send_sms("09220760633", admin_message)  # شماره ادمین

        return JsonResponse({
            'status': 'success',
            'message': 'درخواست شما با موفقیت ثبت شد.'
        })

    except Exception as e:
        logger.error(f"خطا در پردازش درخواست: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'خطا در ثبت درخواست. لطفا دوباره تلاش کنید.'
        }, status=500)


@csrf_exempt
@login_required
def delete_request_view(request, request_id):
    if request.method == 'POST':
        try:
            req = ServiceRequest.objects.get(id=request_id)
            req.delete()
            return JsonResponse({'success': True})
        except ServiceRequest.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'درخواست یافت نشد'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'متد درخواست نامعتبر است'}, status=400)


@csrf_exempt
@login_required
def delete_selected_requests_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request_ids = data.get('ids', [])
            ServiceRequest.objects.filter(id__in=request_ids).delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'متد درخواست نامعتبر است'}, status=400)


def article_detail_view(request, slug):
    article = get_object_or_404(Article, slug=slug, is_active=True)
    return render(request, 'article_detail.html', {'article': article})
