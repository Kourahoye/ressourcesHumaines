from django import forms
from .models import Presence

from django import forms
from .models import Presence

class PresenceForm(forms.ModelForm):
    class Meta:
        model = Presence
        fields = ['employee', 'is_absent']
        widgets = {
            'employee': forms.HiddenInput()
        }
