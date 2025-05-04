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
from .sms import send_sms
import re
import requests  # اضافه کردن import
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from service.sms import send_sms  # مسیر رو بر اساس پروژه خودت اصلاح کن
import json
from .models import Article


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



@csrf_protect
def request_specialist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        service_type = request.POST.get('service_type')

        print(f"دریافت درخواست جدید: {name}, {phone}, {service_type}")

        try:
            # ایجاد درخواست جدید با مدل ServiceRequest
            new_request = ServiceRequest.objects.create(
                name=name,
                phone=phone,
                service_type=service_type,
                status='pending'
            )
            print(f"درخواست با موفقیت ذخیره شد. ID: {new_request.id}")

            # ارسال پیامک به مشتری
            customer_message = f'{name} عزیز، درخواست شما برای {service_type} ثبت شد. با تشکر از شما.'
            customer_data = {
                'to': phone,
                'from': settings.SMS_FROM,
                'text': customer_message
            }
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                response = requests.post(
                    settings.SMS_API_URL,
                    json=customer_data,
                    headers=headers
                )
                print(f"پاسخ خام API پیامک مشتری: {response.text}")
                try:
                    response_data = response.json()
                    print(f"پاسخ JSON API پیامک مشتری: {response_data}")
                    if response.status_code == 200:
                        print("پیامک به مشتری ارسال شد")
                    else:
                        print(f"خطا در ارسال پیامک به مشتری: {response_data}")
                except ValueError as e:
                    print(f"خطا در تبدیل پاسخ به JSON: {e}")
            except Exception as e:
                print(f"خطا در ارسال پیامک به مشتری: {e}")

            # ارسال پیامک به ادمین
            admin_message = f'درخواست جدید از طرف {name} - شماره: {phone} - نوع سرویس: {service_type}'
            admin_data = {
                'to': settings.ADMIN_PHONE,
                'from': settings.SMS_FROM,
                'text': admin_message
            }
            try:
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
                response = requests.post(
                    settings.SMS_API_URL,
                    json=admin_data,
                    headers=headers
                )
                print(f"پاسخ خام API پیامک ادمین: {response.text}")
                try:
                    response_data = response.json()
                    print(f"پاسخ JSON API پیامک ادمین: {response_data}")
                    if response.status_code == 200:
                        print("پیامک به ادمین ارسال شد")
                    else:
                        print(f"خطا در ارسال پیامک به ادمین: {response_data}")
                except ValueError as e:
                    print(f"خطا در تبدیل پاسخ به JSON: {e}")
            except Exception as e:
                print(f"خطا در ارسال پیامک به ادمین: {e}")

            return JsonResponse({
                'status': 'success',
                'message': 'درخواست شما با موفقیت ثبت شد'
            })

        except Exception as e:
            print(f"خطا در ذخیره درخواست: {e}")
            return JsonResponse({
                'status': 'error',
                'message': 'خطا در ثبت درخواست'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'متد درخواست نامعتبر است'
    }, status=400)


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