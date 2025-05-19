from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from autoslug import AutoSlugField


class Request(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    service_type = models.CharField(max_length=20, default='نصب')  # ← مقدار پیش‌فرض
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
        ('done', 'انجام شده')
    ]

    name = models.CharField(max_length=100, verbose_name="نام مشتری")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES, verbose_name="نوع سرویس")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت")

    def __str__(self):
        return f"{self.name} ({self.phone}) - {self.service_type}"


class ArticleSection(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=200, verbose_name='عنوان بخش')
    slug = AutoSlugField(populate_from='title', unique=True, allow_unicode=True, verbose_name='اسلاگ بخش', always_update=False)
    content = models.TextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='articles/sections/', verbose_name='تصویر بخش', null=True, blank=True)
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'بخش مقاله'
        verbose_name_plural = 'بخش‌های مقاله'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.slug}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    slug = AutoSlugField(populate_from='title', unique=True, allow_unicode=True, verbose_name='اسلاگ', always_update=False)
    image = models.ImageField(upload_to='articles/', verbose_name='تصویر مقاله', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ArticleImage(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='album_images')
    image = models.ImageField(upload_to='articles/album/', verbose_name='تصویر آلبوم')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تصویر آلبوم مقاله'
        verbose_name_plural = 'تصاویر آلبوم مقاله'
        ordering = ['uploaded_at']

    def __str__(self):
        return f"آلبوم {self.article.title} - {self.id}"

