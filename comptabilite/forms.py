from django import forms
from employees.models import Employee
from .models import  BonusSlip, Payslip, Salary
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from datetime import date


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'input input-info input-sm w-fulll',
                'placeholder': 'Montant du paiement',
                }),
            'employee': forms.Select(attrs={
                'class': 'select select-info input-sm w-fulll',
                }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            error_class = 'border-red-600'
            field.widget.attrs['class'] = f"{existing_classes} {error_class}" if self.errors.get(field_name) else existing_classes

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('employee'),
                Field('amount'),
                # Submit('submit', 'Enregistrer', css_class="btn btn-ghost btn-outline btn-sm btn-info"),
                css_class="space-y-4"
            )
        )

    def clean(self):
        super().clean()
        
        if self.cleaned_data['amount'] <= 0:
            raise forms.ValidationError("Le montant du paiement doit être supérieur à zéro.")
        return self.cleaned_data


class BonusSlipForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m']
    )
    class Meta:
        model = BonusSlip
        exclude = ['created_by', 'created_at','month','year']
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'select select-info',
                }),
            'amount': forms.NumberInput(attrs={
                'class': 'input input-info',
                'placeholder': 'Montant du paiement',
                }),
            'description': forms.TextInput(attrs={
                'class':'textarea textarea-info',
                'placeholder':'Description de la prime'
                }),
            'date':({
                'class': 'input input-info'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            error_class = 'border-red-600'
            field.widget.attrs['class'] = f"{existing_classes} {error_class}" if self.errors.get(field_name) else existing_classes


        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('employee'),
                Field('amount'),
                Field('date'),
                Field('description'),
                # Submit('submit', 'Enregistrer', css_class="btn btn-ghost btn-outline btn-sm btn-info"),
                css_class="space-y-4"
            )
        )

    def clean(self):
        super().clean()
        
        if self.cleaned_data['amount'] <= 0:
            raise forms.ValidationError("Le montant du paiement doit être supérieur à zéro.")
        return self.cleaned_data
    
    def clean_date(self):
        value = self.cleaned_data['date']
        current_year = date.today().year

        if value.year > current_year:
            raise forms.ValidationError("L'année ne peut pas dépasser l'année actuelle.")
        if value.year < 2010:
            raise forms.ValidationError("L'année ne peut pas être antérieure à 2010.")
        return value



class PaimentForm(forms.ModelForm):
    bonus = forms.DecimalField(
        label="Prime (bonus)",
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=0
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'month'}),
        input_formats=['%Y-%m']
    )
    class Meta:
        model = Payslip
        exclude = ['created_by', 'created_at','month','year','total','generated_by','base_salary']
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'select select-info',
                }),
            'bonus':forms.NumberInput(
                attrs={
                    'class': 'input input-info',
                }
            ),
            'date':forms.DateInput(attrs={
                'class': 'input input-info'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('employee'),
                Field('bonus'),
                Field('date'),
                # Submit('submit', 'Enregistrer', css_class="btn btn-ghost btn-outline btn-sm btn-info"),
                css_class="space-y-4"
            )
        )

    def clean(self):
        super().clean()
        
        if self.cleaned_data['bonus'] < 0:
            raise forms.ValidationError("Le montant du paiement doit être supérieur à zéro.")
        return self.cleaned_data
    
    def clean_employee(self):
        employee = self.cleaned_data.get('employee')

        if not employee or not Employee.objects.filter(pk=employee.pk, user__is_active=True).exists():
            raise forms.ValidationError("L’employé sélectionné n’est pas valide ou a été désactivé.")

        if not Salary.objects.filter(employee=employee).exists():
            raise forms.ValidationError("L’employé sélectionné n’a pas de salaire défini.")

        return employee

    def clean_date(self):
        value = self.cleaned_data['date']
        current_year = date.today().year

        if value.year > current_year:
            raise forms.ValidationError("L'année ne peut pas dépasser l'année actuelle.")
        if value.year < 2010:
            raise forms.ValidationError("L'année ne peut pas être antérieure à 2010.")
        return value