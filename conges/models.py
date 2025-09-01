from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from employees.models import Employee

User = get_user_model()
# Create your models here.
class Conge(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="conges")
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.BooleanField(default=False,null=False,blank=False)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='conges_cree')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="conges_modifies")
    
    def __str__(self):
        return f'conge de {self.employee.user.username} du {self.startDate} au {self.endDate}'
    
    class Meta:
         permissions = [("list_conge", "Can list conges"),("change_conge_status","Can change conges status")]

    
   
class CongesRequest(models.Model):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name="conges_asked")
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(choices=[("pending","Pending"),("aborted","Aborted"),("refused","Refused"),("accepted","Accepted")],null=False,default='pending',max_length=10)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='conges_ask_crees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="conges_ask_modifies")
    
    def __str__(self):
        return f'demande de conge de {self.employee.user.username} du {self.startDate} au {self.endDate}'
    
    class Meta:
        permissions = [("list_congesrequest", "Can list conge s request"),("accept_congesrequest","Can accept conge s request"),("refuse_congesrequest","Can refuse conge s request")]

    def get_absolute_url(self):
        return reverse('conges_request_details', kwargs={'pk': self.pk})