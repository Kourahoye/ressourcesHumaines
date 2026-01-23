from django import forms

from employees.models import Employee
from .models import DepartementHead, Departements
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

class DepartementsForm(forms.ModelForm):

    class Meta:
        model = Departements
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-info w-full',
                'placeholder': 'Nom du département',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du style d'erreur sur les champs
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            error_class = 'border-red-600'
            field.widget.attrs['class'] = f"{existing_classes} {error_class}" if self.errors.get(field_name) else existing_classes

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('name'),
                # Submit('submit', 'Enregistrer', css_class="btn btn-sm btn-info"),
                css_class="space-y-4"
            )
        )
    
    def clean(self):
        super().clean()
        
        if len(self.cleaned_data['name']) < 4:
            raise forms.ValidationError("Le nom du departement est trop court.")



class DepartementHeadFrom(forms.ModelForm):
    # employee = forms.ModelChoiceField(
    #     queryset=Employee.objects.none(),
    #     widget=forms.Select(attrs={
    #         'id':'id_employee',
    #         'class': 'select select-info w-full',
    #     })
    # )
    class Meta:
        model = DepartementHead
        fields = ['departement', 'employee', 'start_date']
        widgets ={
            'departement': forms.Select(attrs={
                'id':'id_departement',
                'class': 'select select-info w-full',
            }),
            'employee': forms.Select(attrs={
                'id':'id_employee',
                'class': 'select select-info w-full',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'input input-info w-full',
                'type': 'date',
            }),
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee'].queryset = Employee.objects.none()
        if self.data.get('employee'):
            self.fields['employee'].queryset = Employee.objects.filter(
                pk=self.data.get('employee')
            )
        # Personnalisation du style d'erreur sur les champs
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            error_class = 'border-red-600'
            field.widget.attrs['class'] = f"{existing_classes} {error_class}" if self.errors.get(field_name) else existing_classes

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('departement'),
                Field('employee'),
                Field('start_date'),
                # Submit('submit', 'Enregistrer', css_class="btn btn-sm btn-info"),
                css_class="space-y-4"
            )
        )
        
    def clean(self):
        cleaned_data = super().clean()
        departement = cleaned_data.get('departement')
        active = cleaned_data.get('active', True)

        if departement and active:
            qs = DepartementHead.objects.filter(
                departement=departement,
                active=True
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    "Il y a déjà un chef de département actif pour ce département."
                )

        return cleaned_data

