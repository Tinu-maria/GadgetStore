from django.contrib.sitemaps import Sitemap
from flipkart_api.models import Product


class SitemapView(Sitemap):
    priority = 0.6
    protocol = 'http'
    changefreq = "weekly"

    def items(self):
        return Product.objects.all()

