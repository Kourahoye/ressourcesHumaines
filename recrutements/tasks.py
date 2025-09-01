from celery import shared_task
from django.utils import timezone
from recrutements.models import Offre

@shared_task
def inactive_expired_offre():
    today = timezone.now().date()
    expired_offers = Offre.objects.filter(date_expiration__lt=today, active=True)
        
    count = expired_offers.count()
        
    if count > 0:
        expired_offers.update(active=False)
        return f'{count} offre(s) expirée(s) ont été désactivée(s)'
    else:
        return 'Aucune offre à désactiver'