from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from departements.models import Departements
from django.core.exceptions import ValidationError

User = get_user_model()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_employee')
    poste = models.CharField(max_length=20)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordonnes')
    date_embauche = models.DateField()
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, related_name='employees')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        permissions = [("list_employee", "Can list employee")]
        # permission_required =['employees.delete_employee']
    def get_absolute_url(self):
        return reverse('employee_profil', kwargs={'pk': self.pk})