from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import Permission
from .models import User


@receiver(post_save, sender=User)
def add_default_permissions(sender, instance, created, **kwargs):
    if not created:
        return

    def assign_permissions():
        default_permission_codenames = [
            # User / profil
            "view_user",
            "view_employee",

            # Organisation
            "view_departements",
            "view_site",

            # Congés
            "view_conge",
            "list_conge",
            "view_congesrequest",

            # Présences
            "view_abcence",
            "view_attendance",

            # Paie
            "view_salary",
            "view_payslip",
            "view_bonus_slip",

            # Informations internes
            "view_message",
            "view_notification",
        ]

        permissions = Permission.objects.filter(
            codename__in=default_permission_codenames
        )

        instance.user_permissions.add(*permissions)

        # purge du cache Django
        instance._perm_cache = None

        # debug sûr
        missing = set(default_permission_codenames) - set(
            permissions.values_list("codename", flat=True)
        )

        if missing:
            print("⚠️ Permissions introuvables :", missing)
        else:
            print(f"✅ Permissions ajoutées à {instance.username}")

    transaction.on_commit(assign_permissions)


@receiver(post_save, sender=User)
def send_notification_user_must_change_password(sender, instance, created, **kwargs):
    # Notifie l'utilisateur de changer son mot de passe à la première connexion
    if created and instance.must_change_password:
        from informations.services import notify_user

        notify_user(
            user=instance,
            title="Changement de mot de passe requis",
            content=(
                "Pour des raisons de sécurité, veuillez changer votre mot de passe lors de votre première connexion."
            ),
        )
        
@receiver(post_save, sender=User)
def send_notif_user_profile_updated(sender, instance, created, **kwargs):
    # Notifie l'utilisateur lorsque son profil est mis à jour
    if not created:
        from informations.services import notify_user

        notify_user(
            user=instance,
            title="Profil mis à jour",
            content=(
                "Votre profil utilisateur a été mis à jour avec succès."
            ),
            link=""
        )