from django import forms
from employees.models import Employee
from .models import Paiment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

class PaimentForm(forms.ModelForm):
    class Meta:
        model = Paiment
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date',
                                           'class':'input input-accent'}),
            'amount': forms.NumberInput(attrs={
                'class': 'input input-primary',
                'placeholder': 'Montant du paiement',
                }),
            'description': forms.Select(attrs={
                'class':'select select-info',
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
                Field('employee'),
                Field('date'),
                Field('amount'),
                Field('description'),
                Submit('submit', 'Enregistrer', css_class="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"),
                css_class="space-y-4"
            )
        )

    def clean(self):
        super().clean()
        
        if self.cleaned_data['amount'] <= 0:
            raise forms.ValidationError("Le montant du paiement doit être supérieur à zéro.")
        return self.cleaned_data