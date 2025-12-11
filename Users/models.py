from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# Create your models here.
from cloudinary.models import CloudinaryField

class User(AbstractUser):
    birthday = models.DateField(null=False, default='2001-01-01')
    avatar = CloudinaryField('avatar', blank=True)  # remplace ImageField
    gender = models.CharField(
        max_length=10,
        choices=[("masculin", "Masculin"), ("feminin", "Feminin")],
        null=False
    )
    must_change_password = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return reverse('userDetail', kwargs={'pk': self.pk})
    
    class Meta:
        permissions = [("list_users", "Can list users")]    