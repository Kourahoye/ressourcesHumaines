from django.db import models
from django.utils.timezone import now
from Users.models import User
from employees.models import Employee

# Create your models here.
class Paiment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='paiments')
    date = models.DateField(default=now(), null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=False)
    description = models.CharField(max_length=50, choices=[
        ('salaire', 'Salaire'),
        ('prime', 'Prime'),
    ],default='salaire', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paiments_created', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paiments_updated', null=True)


    def __str__(self):
        return f"{self.description} de {self.amount} du {self.date} à {self.employee.user}"
    
    class Meta: 
        permissions=[('can_list_paiment', 'Can list paiment')]
        