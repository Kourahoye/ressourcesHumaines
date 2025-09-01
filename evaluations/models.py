from django.db import models
from Users.models import User
from departements.models import Departements
from employees.models import Employee
from django.utils import timezone
from django.db.models import Q

# Create your models here.
class DepartementRating(models.Model):
    departement = models.ForeignKey(Departements, related_name='notes',on_delete=models.CASCADE)
    month = models.CharField(choices=[
        ("Janvier",'Janvier'),("Fevrier",'Fevrier'),("Mars",'Mars'),("Avril",'Avril'),("Mai",'Mai'),("Juin",'Juin'),("Juillet",'Juillet'),("Aout",'Aout'),("Septembre",'Septembre'),("Octobre",'Octobre'),("Novembre",'Novembre'),("Decembre",'Decembre'),
         ],null=False,max_length=10,
         default=f"{timezone.now().month}"
    )
    year = models.CharField(null=False,default=f"{timezone.now().year}",max_length=6)
    note = models.PositiveIntegerField(null=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='departement_evaluyee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="evaluation_departemen_modifies")

    class Meta:
        permissions = [('list_departementRating','can list departement notes')]
        constraints =[
            models.UniqueConstraint(fields=['departement','month','year'], name="UniqueConstraint_date_departement",violation_error_message="Ce departement est deja evaluer"),
            models.CheckConstraint(condition=Q(note__lte=10),name="dept_note_lte_10",violation_error_message="La note maximale est 10"),
            models.CheckConstraint(condition=Q(note__gte=0),name="dept_note_gte_10",violation_error_message="La note minimale est 0"),
        ]
        


    def __str__(self):
       return f'Note du departement {self.departement.name} du month {self.month}'

class EmployeeRating(models.Model):
    employee = models.ForeignKey(Employee, related_name='notes',on_delete=models.CASCADE)
    month = models.CharField(choices=[
        ("Janvier",'Janvier'),("Fevrier",'Fevrier'),("Mars",'Mars'),("Avril",'Avril'),("Mai",'Mai'),("Juin",'Juin'),("Juillet",'Juillet'),("Aout",'Aout'),("Septembre",'Septembre'),("Octobre",'Octobre'),("Novembre",'Novembre'),("Decembre",'Decembre'),
         ],null=False,max_length=10,
         default=f"{timezone.now().month}"
    )
    year = models.CharField(null=False,default=f"{timezone.now().year}",max_length=6)
    note = models.PositiveIntegerField(null=False,)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='employee_evaluyee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="evaluation_employee_modifies")

    class Meta:
        permissions = [('list_employeeRating','can list employee notes')]
        constraints =[
            models.UniqueConstraint(fields=['month','employee','year'], name="UniqueConstraint_date_employee",violation_error_message="Cet employer est deja evaluer"),
            models.CheckConstraint(condition=Q(note__lte=10),name="emp_note_lte_10",violation_error_message="La note maximale est 10"),
            models.CheckConstraint(condition=Q(note__gte=0),name="emp_note_gte_10",violation_error_message="La note minimale est 0")
            ]
        

    def __str__(self):
       return f'Note du employee {self.employee.user} du month {self.month}'
