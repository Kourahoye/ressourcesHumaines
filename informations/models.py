# models.py
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models

from Users.models import User
from departements.models import Departements


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    departement = models.ForeignKey(Departements,on_delete=models.CASCADE,related_name="ciculaires")
    subject = models.CharField(max_length=255)
    content_html = CKEditor5Field(config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Notification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # Utilisateur cible
    to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # Lien dynamique (url + params éventuels)
    link = models.JSONField(
        help_text="Ex: {'url_name': 'offre_detail', 'kwargs': {'pk': 3}}",null=True,blank=True
    )

    # Statut
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} → {self.to.username}"
    
    def get_url(self):
        if not self.link:
            return None
        return reverse(
            self.link["url_name"],
            kwargs=self.link.get("kwargs", {})
        )
