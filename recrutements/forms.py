from django import forms
from .models import Offre, Candidat, Postulation

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'description', 'date_expiration', 'departement']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'input input-info w-full dark:text-white',
                'placeholder': "Titre de l'offre",
            }),
            'description': forms.Textarea(attrs={
                'class': 'input input-info w-full dark:text-white',
                'placeholder': "Description",
            }),
            'date_expiration': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'input input-info w-full dark:text-white',
                },
                format='%Y-%m-%dT%H:%M'
            ),

            'departement': forms.Select(attrs={
                'class': 'select select-info w-full dark:text-white',
            }),
        }

class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = [
            'nom', 'prenom', 'email', 'telephone',
            'cv', 'lettre_motivation', 'genre',
            'date_naissance', 'niveau'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'input input-info w-full', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'input input-info w-full', 'placeholder': 'Prénom'}),
            'email': forms.EmailInput(attrs={'class': 'input input-info w-full', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'input input-info w-full', 'placeholder': 'Téléphone'}),
            'cv': forms.ClearableFileInput(attrs={'class': 'file-input file-input-info w-full'}),
            'lettre_motivation': forms.Textarea(attrs={'class': 'textarea textarea-info w-full', 'placeholder': 'Lettre de motivation (optionnel)'}),
            'genre': forms.Select(attrs={'class': 'select select-info w-full'}),
            'date_naissance': forms.DateInput(attrs={'class': 'input input-info w-full', 'type': 'date'}),
            'niveau': forms.Select(attrs={'class': 'select select-info w-full'}),
        }

class PostulationForm(forms.ModelForm):
    class Meta:
        model = Postulation
        fields = ['remarque']
        widgets = {
            'remarque': forms.Textarea(attrs={'class': 'textarea textarea-info w-full', 'placeholder': 'Remarque (optionnel)'}),
        }



class PostulationAdminForm(forms.ModelForm):
    class Meta:
        model = Postulation
        fields = ['statut', 'remarque']
        widgets = {
            'statut': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'remarque': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 4}),
        }
