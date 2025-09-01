from django.db import models
from django.contrib.auth import get_user_model
from employees.models import Employee


User = get_user_model()
# Create your models here.
class Abcence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='absences')
    date = models.DateField(null=False)
    is_absent = models.BooleanField(null=False, choices=[
        (True, "Absent"),
        (False, "Présent")
    ],default=True)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.user}  {'absent' if self.is_absent else 'présent'} le {self.created_at}"

    class Meta:
         constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_presence_per_employee_date',violation_error_message="Un employé ne peut pas avoir plusieurs présences pour la même date.")
         ]
         permissions = [("list_presence", "Can list presences")]