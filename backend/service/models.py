from django.db import models
from django.utils import timezone


class Request(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"


class ServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('install', 'نصب'),
        ('repair', 'تعمیر')
    ]

    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('approved', 'تایید شده'),
        ('done', 'انجام شده')
    ]

    name = models.CharField(max_length=100, verbose_name="نام مشتری")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES, verbose_name="نوع سرویس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")

    def __str__(self):
        return f"{self.name} ({self.phone}) - {self.service_type}"

