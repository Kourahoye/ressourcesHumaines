# Users/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.conf import settings

from .models import User


@receiver(post_save, sender=User)
def add_default_permissions(sender, instance, created, **kwargs):
    
    #Ajoute des permissions par défaut à chaque nouvel utilisateur.
    
    if not created:
        return  

    try:
        default_permission_codenames = [
            "view_user",
            "list_users",
            "view_employee",
            "list_employee",
            "view_conge",
            "list_conges",
            "view_departements",
            "list_departements",
            "view_site",
            "view_attendance",
            "view_salary",
            "view_payslip",

        ]


        permissions = Permission.objects.filter(codename__in=default_permission_codenames)

        instance.user_permissions.add(*permissions)

        # (optionnel) — si tu veux ajouter automatiquement des groupes :
        # from django.contrib.auth.models import Group
        # group = Group.objects.get(name="Employés")
        # instance.groups.add(group)

    except Permission.DoesNotExist:
        print("⚠️ Certaines permissions par défaut n'ont pas été trouvées.")
    except Exception as e:
        print(f"Erreur lors de l'ajout des permissions par défaut : {e}")

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