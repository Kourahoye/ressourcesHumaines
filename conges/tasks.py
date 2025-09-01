from celery import shared_task
from datetime import date
from .models import Conge

@shared_task(name="conges.tasks.check_finished_conges")
def check_finished_conges():
    """
    Celery task to check and inactivate conges that have ended
    """
    today = date.today()
    # Get all active conges that have end dates before today
    finished_conges = Conge.objects.filter(
        status=True,
        endDate__lt=today
    )
    
    # Update their status to inactive
    updated_count = finished_conges.update(status=False)
    
    return f"Updated {updated_count} finished conges to inactive status"