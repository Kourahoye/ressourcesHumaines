from celery import shared_task
from datetime import date
from django.contrib.auth import get_user_model
from employees.models import Employee
from presences.models import Abcence
from presences.guinea_calendar import GuineaCalendar

User = get_user_model()

@shared_task
def verifier_absences_quotidiennes():
    today = date.today()
    cal = GuineaCalendar()

    if not cal.is_working_day(today):
        return f"{today} n'est pas un jour travaillé"

    try:
        print("=== APPROCHE QUERYSET ===")

        employees_absents = (
            Employee.objects.filter(user__is_active=True)  # 🔒 on verrouille sur les actifs
            .exclude(conges__startDate__lte=today, conges__endDate__gte=today, conges__status=True)
            .exclude(attendances__date=today)
            .exclude(absences__date=today)
            .filter(user__is_active=True)   
        )

        absents_a_creer = [Abcence(employee=emp, date=today, is_absent=True) for emp in employees_absents]

        if absents_a_creer:
            Abcence.objects.bulk_create(absents_a_creer)
            print(f"{len(absents_a_creer)} absences créées")
        else:
            print("Aucune absence à créer")

        return f"{len(absents_a_creer)} employés actifs marqués absents"

    except Exception as e:
        print(f"ERREUR: {str(e)}")
        return f"Erreur: {str(e)}"
