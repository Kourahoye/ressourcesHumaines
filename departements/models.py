from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
# Create your models here.
class Departements(models.Model):
    name = models.CharField(max_length=50,null=False,unique=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='departements_cree')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="departement_modifies")
    
    def __str__(self):
        return self.name
    
    class Meta:
         permissions = [("list_departement", "Can list departements")]

    def get_absolute_url(self):
        return reverse('departements_profil', kwargs={'pk': self.pk})