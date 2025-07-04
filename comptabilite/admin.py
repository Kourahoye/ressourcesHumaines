from django.contrib import admin

from .models import  BonusSlip, Payslip, Salary

# Register your models here.
admin.site.register([Salary,Payslip,BonusSlip])