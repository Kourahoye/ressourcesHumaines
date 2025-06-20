from django.contrib import admin

from evaluations.models import DepartementRating, EmployeeRating

# Register your models here.
admin.site.register(EmployeeRating)
admin.site.register(DepartementRating)