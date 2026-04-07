from django.core.management.base import BaseCommand
from django.utils import timezone
from recrutements.models import Offre


class Command(BaseCommand):
    help = 'Vérifie les offres expirées et les désactive'

    def handle(self, *args, **options):
        today = timezone.now()
        expired_offers = Offre.objects.filter(date_expiration__lte=today, active=True)
        
        count = expired_offers.count()
        
        if count > 0:
            expired_offers.update(active=False)
            self.stdout.write(self.style.SUCCESS(f'{count} offre{"s" if count>1 else ""} expirée{"s" if count>1 else ""} ont été désactivée{"s" if count>1 else ""}'))
        else:
            self.stdout.write('Aucune offre à désactiver')