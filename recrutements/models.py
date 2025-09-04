from django.db import models
from django.contrib.auth import get_user_model
from departements.models import Departements
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
User = get_user_model()

# Exemple de niveau d'études ou expériences
class Niveau(models.TextChoices):
    LICENCE = 'licence', 'Licence'
    MASTER = 'master', 'Master'
    DOCTORAT = 'doctorat', 'Doctorat'

# 📌 Offre d'emploi
class Offre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    date_expiration = models.DateTimeField(default=timezone.now)  
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, related_name='offres')
    active = models.BooleanField(default=True,null=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='offres_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='offres_updated')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [("list_offre", "Can list offre"),]

    def __str__(self):
        return self.titre

# 👤 Candidat
class Candidat(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    cv = CloudinaryField('cv_files/', resource_type='raw', validators=[FileExtensionValidator(['pdf'])])
    lettre_motivation = models.TextField(blank=True)
    genre = models.CharField(max_length=10, choices=[("masculin", "Masculin"), ("feminin", "Féminin")])
    date_naissance = models.DateField()
    niveau = models.CharField(choices=Niveau.choices, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        
        permissions = [
            ("list_candidat", "Can list candidat"),
        ]

    def __str__(self):
        return f"{self.prenom} {self.nom}"

# 📄 Postulation
class Postulation(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='postulations')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE, related_name='postulations')
    date_postulation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('rejete', 'Rejeté'),
    ], default='en_attente')
    remarque = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        #constrain unique par offre
         permissions = [
            ("list_postulation", "Can list postulation"),
        ]

    def __str__(self):
        return f"{self.candidat} → {self.offre}"
