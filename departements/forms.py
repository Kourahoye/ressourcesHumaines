from django import forms
from .models import Departements
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

class DepartementsForm(forms.ModelForm):

    class Meta:
        model = Departements
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 rounded-md border-2 border-black shadow-sm',
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
                Submit('submit', 'Enregistrer', css_class="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"),
                css_class="space-y-4"
            )
        )
    
    def clean(self):
        super().clean()
        
        if len(self.cleaned_data['name']) < 4:
            raise forms.ValidationError("Le nom du departement est trop court.")
