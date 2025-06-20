from django.db import models
from django.contrib.auth import get_user_model
from employees.models import Employee


User = get_user_model()
# Create your models here.
class Presence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField(null=False)
    is_absent = models.BooleanField(null=False, choices=[
        (True, "Absent"),
        (False, "Présent")
    ])
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rapport_de_presence')
    
    def __str__(self):
        return f"{self.employee.user}  {'présent' if self.is_absent else 'absent'} le {self.created_at}"

    class Meta:
         constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_presence_per_employee_date',violation_error_message="Un employé ne peut pas avoir plusieurs présences pour la même date.")
         ]
         permissions = [("list_presence", "Can list presences")]