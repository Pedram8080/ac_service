from django.contrib.sitemaps import Sitemap
from .models import Article


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ['home', 'about', 'article']

    def location(self, item):
        if item == 'home':
            return '/'
        elif item == 'about':
            return '/about/'
        elif item == 'article':
            return '/article/'


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/article/{obj.slug}/"
