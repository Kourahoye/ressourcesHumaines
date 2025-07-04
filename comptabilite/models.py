from decimal import Decimal
from django.db import models
from Users.models import User
from employees.models import Employee
from django.core.validators import MaxValueValidator, MinValueValidator


class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="salary")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salaries_created', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salaries_updated', null=True)


    class Meta:
        verbose_name_plural = 'salaries'
        permissions=[('can_list_salary', 'Can list salary')]

    def __str__(self):
        return f"Salary of {self.employee}"

class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payslips")
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    base_salary = models.DecimalField(max_digits=15, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payslips_generated', null=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'month', 'year'], name='unique_employee_month_year')
        ]

    def __str__(self):
        return f"Fiche de paie : {self.employee} - {self.month}/{self.year}"
    
    def save(self, *args, **kwargs):
        # Calcul automatique du total avant sauvegarde
        self.total = (self.base_salary or Decimal('0.00')) + (self.bonus or Decimal('0.00'))
        super().save(*args, **kwargs)
    

class BonusSlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="bonus_slips")
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    year = models.IntegerField(validators=[MinValueValidator(2000)])
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.CharField(max_length=30,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonusslips_generated', null=True)

    def __str__(self):
        return f"Fiche de prime : {self.employee} - {self.month}/{self.year}"