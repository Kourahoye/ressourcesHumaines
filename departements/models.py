from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# from employees.models import Employee

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
    
    
class DepartementHead(models.Model):
    departement = models.ForeignKey(Departements,on_delete=models.CASCADE,related_name='departement_heads')
    employee = models.ForeignKey("employees.Employee",on_delete=models.CASCADE,related_name='employee_departement_heads')
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='departement_heads_cree')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="departement_head_modifies")
    
    def __str__(self):
        return f"{self.employee} - {self.departement}"
    
    class Meta:
        permissions = [("assign_departement_head", "Can assign departement head")]
        constraints = [
            models.UniqueConstraint(
                fields=['departement'],
                condition=models.Q(active=True),
                name='unique_active_departement_head',
                violation_error_message="Il y a déjà un chef de département actif pour ce département.Desactivez l'ancien avant d'en ajouter un nouveau."
            ),
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F('start_date')),
                name='end_date_after_start_date',violation_error_message="La date de fin ne peut pas être antérieure à la date de début."
            )
        ]
    