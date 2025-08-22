from celery import shared_task
from django.core.management.base import BaseCommand
from datetime import date
from conges.models import Conge
from employees.models import Employee
from attendances.models import Attendance
from presences.guinea_calendar import GuineaCalendar
from presences.models import Abcence
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Vérifie les abcences quotidiennes en Guinée'

    def handle(self, *args, **options):
        result = verifier_absences_quotidiennes()
        self.stdout.write(self.style.SUCCESS(result))

@shared_task
def verifier_absences_quotidiennes():
    today = date.today()
    cal = GuineaCalendar()

    if not cal.is_working_day(today):
        return f"{today} n'est pas un jour travaillé"

    try:
        employees_absents = (
            Employee.objects.filter(user__is_active=True)
            .exclude(conges__startDate__lte=today, conges__endDate__gte=today, conges__status=True)
            .exclude(attendances__date=today)
            .exclude(absences__date=today)
            .filter(user__is_active=True)
        )

        absents_a_creer = [Abcence(employee=emp, date=today, is_absent=True) for emp in employees_absents]

        if absents_a_creer:
            Abcence.objects.bulk_create(absents_a_creer)
            return f"{len(absents_a_creer)} employés actifs marqués absents"
        else:
            return "Aucune absence à créer"

    except Exception as e:
        return f"Erreur: {str(e)}"
