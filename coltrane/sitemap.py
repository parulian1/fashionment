from django.contrib.sitemaps import Sitemap
from coltrane.models import FashionFacts

class ColtraneSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5
    def items(self):
        return FashionFacts.objects.all()