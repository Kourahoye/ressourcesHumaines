from django import forms
from conges.models import Conge, CongesRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div


class CongeRequestForm(forms.ModelForm):

 
    class Meta:
        model = CongesRequest
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by','status','employee']
        widgets = {
            'startDate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-info input-sm  w-full',
            }),
            'endDate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-info input-sm w-full',
            }),
         }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du style d'erreur sur les champs
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            error_class = 'alert alert-error'
            field.widget.attrs['class'] = f"{existing_classes} {error_class}" if self.errors.get(field_name) else existing_classes

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('startDate',css_class="input input-info"),
                Field('endDate',css_class="input input-info"),
                Field('employee',css_class="select select-info"),
                # Submit('submit', 'Enregistrer', css_class="m-3 btn btn-info btn-sm"),
                css_class="space-y-4"
            )
        )
    
    def clean(self):
        cleaned_data = super().clean()
        startDate = cleaned_data.get('startDate')
        endDate = cleaned_data.get('endDate')
        
        if startDate > endDate:
            raise forms.ValidationError("Debut doit venir avant la fin.")


class CongeForm(forms.ModelForm):

 
    class Meta:
        model = Conge
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at', 'updated_by','status']
        widgets = {
            'startDate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-info w-full',
            }),
            'endDate': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input input-info w-full',
            }),
            'employee': forms.Select(attrs={
                'class': 'select select-info input-sm w-full',
            }),
         }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personnalisation du style d'erreur sur les champs
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            error_class = 'alert alert-error'
            field.widget.attrs['class'] = f"{existing_classes} {error_class}" if self.errors.get(field_name) else existing_classes

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('employee',css_class="select select-info"),
                Field('startDate',css_class="input input-info"),
                Field('endDate',css_class="input input-info"),
                # Submit('submit', 'Enregistrer', css_class="btn btn-sm btn-info"),
                css_class="space-y-4 dark:text-white"
            )
        )
    
    def clean(self):
        cleaned_data = super().clean()
        startDate = cleaned_data.get('startDate')
        endDate = cleaned_data.get('endDate')
        
        if startDate > endDate:
            raise forms.ValidationError("Debut doit venir avant la fin.")