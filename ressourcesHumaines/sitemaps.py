from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        # Ce sont les noms de tes URL nommées (name="...")
        return ["dashbord", "offre-list","liste_departements","departements_notes"]

    def location(self, item):
        return reverse(item)
