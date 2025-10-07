from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # Ce sont les noms de tes URL nommées (name="...")
        return ["dashbord", "recrutements"]

    def location(self, item):
        return reverse(item)
