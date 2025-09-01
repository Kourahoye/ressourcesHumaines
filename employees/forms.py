from django.utils import timezone
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        exclude = ['created_at', 'created_by']
        widgets = {
            'date_embauche': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-info w-full',
            }),
            'user': forms.Select(attrs={
                'class': 'select select-info w-full',
            }),
            'poste': forms.TextInput(attrs={
                'class': 'input input-info w-full',
            }),
            'manager': forms.Select(attrs={
                'class': 'select select-info w-full',
            }),
            'departement': forms.Select(attrs={
                'class': 'select select-info w-full',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_embauche = cleaned_data.get('date_embauche')
        manager = cleaned_data.get('manager')
        departement = cleaned_data.get('departement')
        user = cleaned_data.get('user')

        if date_embauche and date_embauche > timezone.now().date():
            self.add_error('date_embauche', "La date d'embauche ne peut pas être dans le futur.")

        if manager:
            if user and manager == user:
                self.add_error('manager', "Un employé ne peut pas être son propre manager.")

            if manager.departement != departement:
                self.add_error('manager', "Le manager doit appartenir au même département que l'employé.")
