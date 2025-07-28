from django.contrib import admin

from recrutements.models import Postulation,Offre,Candidat

# Register your models here.
admin.site.register([Candidat,Offre,Postulation])