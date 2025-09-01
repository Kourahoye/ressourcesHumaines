from django import forms
from .models import Abcence

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Abcence
        fields = ['employee']
        widgets = {
            'employee': forms.TextInput(attrs={'class': 'input input-info w-full'}),
        }
