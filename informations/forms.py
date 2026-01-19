# forms.py
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from departements.models import Departements
from .models import Message
from Users.models import User
class MessageForm(forms.ModelForm):

    subject = forms.CharField(max_length=255)
    # content_html = forms.CharField(widget=CKEditor5Widget())
    
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
        #   self.fields["content_html"].required = False
    
    class Meta:
        model = Message
        fields = ['subject','content_html','departement']
        widgets = {
            'content_html': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, config_name='extends'
            ),
            'subject': forms.TextInput(attrs={'class': 'w-full'}),
            'departement': forms.Select(attrs={'class': 'w-full'}),
        }
