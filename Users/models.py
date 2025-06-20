from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=False,default='2001-01-01')
    avatar = models.ImageField(upload_to='avatars/',blank=True,null=False)
    gender = models.CharField(null=False,choices=[("masculin","Masculin"),("feminin","Feminin")],max_length=10)
    
    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return reverse('userDetail', kwargs={'pk': self.pk})
    
    class Meta:
        permissions = [("list_users", "Can list users")]    