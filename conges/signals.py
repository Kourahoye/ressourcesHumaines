from django.db.models.signals import post_save
from django.dispatch import receiver

from informations.services import notify_user

from .models import Conge, CongesRequest


@receiver(post_save, sender=CongesRequest)
def conges_request_update_notification(sender, instance, created, **kwargs):
    # On ne notifie que lors d'une mise à jour
    if created:
        return

    if not instance.created_by:
        return

    status_messages = {
        "accepted": "Votre demande de congé a été acceptée.",
        "refused": "Votre demande de congé a été refusée.",
        "aborted": "Votre demande de congé a été annulée.",
        "pending": "Votre demande de congé est en attente de validation.",
    }

    message = status_messages.get(
        instance.status,
        "Le statut de votre demande de congé a été mis à jour."
    )

    notify_user(
        user=instance.created_by,
        title="Mise à jour de la demande de congé",
        content=(
            f"{message}\n"
            f"Période : du {instance.startDate} au {instance.endDate}."
        ),
        link={
            "url_name": "conges_request_details",
            "kwargs": {"pk": instance.pk}
        }
    )

@receiver(post_save,sender=Conge)
def conge_gifted_notification(sender,instance,created,**kwargs):
    if created:
        if not instance.employee or not instance.employee.user:
            return

        notify_user(
            user=instance.employee.user,
            title="Congé attribué",
            content=(
                f"Un congé de {instance.number_of_days()} jours vous a été attribué "
                f"du {instance.startDate} au {instance.endDate}."
            ),
            link=""
            # link={
            #     "url_name": "conge_details",
            #     "kwargs": {"pk": instance.pk}
            # }
        )
