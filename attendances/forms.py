from django import forms
from .models import Presence

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['employee']
        widgets = {
            'employee': forms.TextInput(attrs={'class': 'input input-info w-full'}),
        }
