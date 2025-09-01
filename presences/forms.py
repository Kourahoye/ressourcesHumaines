from django import forms
from .models import Abcence

from django import forms
from .models import Abcence

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Abcence
        fields = ['employee', 'is_absent']
        widgets = {
            'employee': forms.HiddenInput()
        }
