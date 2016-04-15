from django.contrib.sitemaps import Sitemap
from store.models import Store, Item,LineCategory, Line

class StoreSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Store.objects.all()

class ItemSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Item.objects.all()

class LineSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Line.objects.all()
