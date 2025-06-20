from django import forms
from django.utils import timezone
from evaluations.models import DepartementRating, EmployeeRating
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

class DepartementRateForm(forms.ModelForm):
    # note = forms.IntegerField(min_value=0,max_value=10,required=True)

    class Meta:
        model = DepartementRating
        fields = "__all__"
        exclude = ['created_at', 'created_by','updated_at', 'updated_by']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'month',
                'class': 'input input-primary w-full',
            }),
            'departement': forms.Select(attrs={
                'class': 'select select-accent w-full',
            }),
            'month': forms.Select(attrs={
                'class': 'select select-accent w-full',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'input input-accent w-full',
            }),
            'note': forms.NumberInput(attrs={
                'min':'0',
                'max':'10',
                'class': 'input input-accent w-full',
            }),
        }
    


    from django.utils import timezone
from django.core.exceptions import ValidationError

def clean(self):
    months = {
        1: 'Janvier',
        2: 'Fevrier',
        3: 'Mars',
        4: 'Avril',
        5: 'Mai',
        6: 'Juin',
        7: 'Juillet',
        8: 'Aout',
        9: 'Septembre',
        10: 'Octobre',
        11: 'Novembre',
        12: 'Decembre'
    }

    cleaned_data = super().clean()
    month = cleaned_data.get('month')
    year = cleaned_data.get('year')
    note = cleaned_data.get('note')

    if month and year:
        # Inverser le dictionnaire pour retrouver le numéro du mois
        months_inverse = {v: k for k, v in months.items()}
        current_date = timezone.now()

        try:
            month_num = months_inverse[month]
            year_num = int(year)

            # Comparer avec la date actuelle
            if year_num > current_date.year or (year_num == current_date.year and month_num > current_date.month):
                self.add_error('month', "La date ne peut pas être dans le futur.")
                self.add_error('year', "La date ne peut pas être dans le futur.")
        except (KeyError, ValueError):
            self.add_error('month', "Mois invalide.")
            self.add_error('year', "Année invalide.")

    if note is not None and (note < 0 or note > 10):
        self.add_error('note', "La note doit être comprise entre 0 et 10.")

            


class EmployeeRateForm(forms.ModelForm):
    # note = forms.IntegerField(min_value=0,max_value=10,required=True,widget=forms.NumberInput)

    class Meta:
        model = EmployeeRating
        fields = "__all__"
        exclude = ['created_at', 'created_by','updated_at', 'updated_by']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'month',
                'class': 'input input-primary w-full',
            }),
            'employee': forms.Select(attrs={
                'class': 'select select-accent w-full',
            }),
            'month': forms.Select(attrs={
                'class': 'select select-accent w-full',
            }),
            'year': forms.NumberInput(attrs={
                'class': 'input input-accent w-full',
            }),
            'note': forms.NumberInput(attrs={
                'min':'0',
                'max':'10',
                'class': 'input input-accent w-full',
            }),
        }

    from django.utils import timezone
from django.core.exceptions import ValidationError

def clean(self):
    months = {
        1: 'Janvier',
        2: 'Fevrier',
        3: 'Mars',
        4: 'Avril',
        5: 'Mai',
        6: 'Juin',
        7: 'Juillet',
        8: 'Aout',
        9: 'Septembre',
        10: 'Octobre',
        11: 'Novembre',
        12: 'Decembre'
    }

    cleaned_data = super().clean()
    month = cleaned_data.get('month')
    year = cleaned_data.get('year')
    note = cleaned_data.get('note')

    if month and year:
        # Inverser le dictionnaire pour retrouver le numéro du mois
        months_inverse = {v: k for k, v in months.items()}
        current_date = timezone.now()

        try:
            month_num = months_inverse[month]
            year_num = int(year)

            # Comparer avec la date actuelle
            if year_num > current_date.year or (year_num == current_date.year and month_num > current_date.month):
                self.add_error('month', "La date ne peut pas être dans le futur.")
                self.add_error('year', "La date ne peut pas être dans le futur.")
        except (KeyError, ValueError):
            self.add_error('month', "Mois invalide.")
            self.add_error('year', "Année invalide.")

    if note is not None and (note < 0 or note > 10):
        self.add_error('note', "La note doit être comprise entre 0 et 10.")

