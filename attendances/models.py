from django.db import models
from django.conf import settings
from django.utils import timezone

from employees.models import Employee

class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    date = models.DateField(default=timezone.now)
    heure_arrivee = models.TimeField(null=True, blank=True)
    heure_depart = models.TimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=['employee', 'date'],
            name='unique_employee_date',
            violation_error_message='Attendance for this employee on this date already exists.'
            )
        ]
        # ordering = ['-date']

    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"
