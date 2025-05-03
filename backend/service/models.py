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
        ('done', 'انجام شده'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"

