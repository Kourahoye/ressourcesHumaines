from django.db.models.signals import post_save
from django.dispatch import receiver
from informations.models import Notification

from comptabilite.models import BonusSlip, BonusSlip, Payslip, Salary


@receiver(post_save,sender=Salary)
def salary_notify(sender,instance,created,**kwargs):
    if created:
        # Logic to notify the employee about their salary creation
        employee_user = instance.employee.user
        # Assuming there is a Notification model similar to the evaluations app
        Notification.objects.create(
            to=employee_user,
            title="Création de salaire",
            content=f"Votre salaire a été créé avec un montant de {instance.amount}.",
            # link={
            #     "url_name": "salary_detail",
            #     "kwargs": {"pk": instance.pk}
            # }
        )
    else:
        # Logic to notify the employee about their salary update
        employee_user = instance.employee.user
        Notification.objects.create(
            to=employee_user,
            title="Mise à jour de salaire",
            content=f"Votre salaire a été mis à jour avec un nouveau montant de {instance.amount}.",
            # link={
            #     "url_name": "salary_detail",
            #     "kwargs": {"pk": instance.pk}
            # }
        )

@receiver(post_save,sender=Payslip)
def payslip_notify(sender,instance,created,**kwargs):
    if created:
        # Logic to notify the employee about their new payslip
        employee_user = instance.employee.user
        Notification.objects.create(
            to=employee_user,
            title="Nouveau paiement",
            content=f"Une nouvelle fiche de paie pour {instance.month}/{instance.year} a été générée avec un total de {instance.total}.",
            link={
                "url_name": "payslip_detail",
                "kwargs": {"pk": instance.pk}
            }
        )

@receiver(post_save,sender=BonusSlip)
def bonus_notify(sender,instance,created,**kwargs):
    if created:
        # Logic to notify the employee about their new bonus slip
        employee_user = instance.employee.user
        Notification.objects.create(
            to=employee_user,
            title="Paiment de prime",
            content=f"Nouvelle prime pour {instance.month}/{instance.year} a été créée avec un montant de {instance.amount}.",
            link={
                "url_name": "bonus_details",
                "kwargs": {"pk": instance.pk}
            }
        )