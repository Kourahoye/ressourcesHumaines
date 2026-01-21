from django.db.models.signals import post_save
from django.dispatch import receiver

from informations.models import Notification

from  .models import DepartementRating, EmployeeRating

@receiver(post_save,sender=DepartementRating)
def notify_departement_rating(sender,instance,created,**kwargs):
    if created:
        # Logic to notify relevant users about the new department rating
        # find the all active employee departement  and send notification
        employes = instance.departement.employees.filter(user__is_active=True)
        # use bulk create to create notification for all employes
        Notification.objects.bulk_create(
            [
                Notification(
                    to=employe.user,
                    title="Evaluation sur le département",
                    content=f"Votre departement a ete evaluer avec une note de {instance.note}.",
                    # link={
                    #     "url_name": "departement_detail",
                    #     "kwargs": {"pk": instance.departement.pk}
                    # }
                )
                for employe in employes
            ]
        )
        
@receiver(post_save,sender=EmployeeRating)
def notify_employee_rating(sender,instance,created,**kwargs):
    if created:
        # Logic to notify the employee about their new rating
        Notification.objects.create(
            to=instance.employee.user,
            title="Evaluation individuelle",
            content=f"Vous avez ete evaluer avec une note de {instance.note} au moi de {instance.month }-{instance.year}.",
            # link={
            #     "url_name": "employee_profile",
            #     "kwargs": {"pk": instance.employee.pk}
            # }
        )