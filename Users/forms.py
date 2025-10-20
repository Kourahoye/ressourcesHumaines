
from django import forms

from Users.models import User


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Pseudo",required=True)
    last_name = forms.CharField(label="Nom")
    first_name = forms.CharField(label="Prénom")
    email = forms.EmailField(label="Email", widget=forms.EmailInput,required=True)
    avatar = forms.ImageField(label="Image", widget=forms.FileInput,required=True,allow_empty_file=False)
    birthday = forms.CharField(label="Date de naissance",widget=forms.DateInput(attrs={'type':'date'}),required=True)
    gender = forms.ChoiceField(label='Genre', widget=forms.RadioSelect,choices=[("masculin","Masculin"),("feminin","Feminin")])
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput,required=True)
    class Meta:
        model = User
        labels = ['Nom utilisateur','Nom','Prenom', 'Email', 'Mot de passe','Avatar','Genre']
        fields = ('username','last_name','first_name','email','birthday','password','avatar','gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full input input-info',
                                                     'id': 'username'})
        self.fields['last_name'].widget.attrs.update({'class': 'w-full input input-info',
                                                     'id': 'last_name'})
        self.fields['first_name'].widget.attrs.update({'class': 'w-full input input-info',
                                                     'id': 'first_name'})
        self.fields['email'].widget.attrs.update({'class': 'w-full input input-info',
                                                  'id': 'email'})
        self.fields['avatar'].widget.attrs.update({'class': 'w-full file-input file-input-info',
                                                  'id': 'avatar'})
        self.fields['birthday'].widget.attrs.update({'class': 'w-full input input-info',
                                                  'id': 'birthday'})
        self.fields['password'].widget.attrs.update({'class': 'w-full input input-info',
                                                     'id': 'password'})
        self.fields['gender'].widget.attrs.update({'class': 'rounded-full p-1 border-transparent',
                                                 'id': 'gender'})

class LoginForm(forms.Form):
    username = forms.CharField(label="Username",required=True)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput,required=True)

    class Meta:
        model = User
        labels = ['Nom utilisateur','Mot de passe']
        fields = ('username','password')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                     'id': 'username'})
        self.fields['password'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                     'id': 'password'})
    

class UserUpdateForm(forms.ModelForm):
    error_css_class = 'text-red-600 text-sm font-semibold'
    # error_class = 'text-red-600 text-sm font-semibold'
    username = forms.CharField(label="Pseudo",required=True)
    last_name = forms.CharField(label="Nom")
    first_name = forms.CharField(label="Prénom")
    email = forms.EmailField(label="Email", widget=forms.EmailInput,required=True)
    avatar = forms.ImageField(label="Image", widget=forms.FileInput,required=True,allow_empty_file=False)
    birthday = forms.CharField(label="Date de naissance",widget=forms.DateInput(attrs={'type':'date'}),required=True)
    gender = forms.ChoiceField(label='Genre', widget=forms.RadioSelect,choices=[("masculin","Masculin"),("feminin","Feminin")])
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput,required=True)

    class Meta:
        model = User
        labels = ['Nom utilisateur','Nom','Prenom', 'Email','Avatar','Genre']
        fields = ('username','last_name','first_name','email','birthday','avatar','gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input input-info input-sm w-full',
                                                     'id': 'username'})
        self.fields['last_name'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                     'id': 'last_name'})
        self.fields['first_name'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                     'id': 'first_name'})
        self.fields['email'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                  'id': 'email'})
        self.fields['avatar'].widget.attrs.update({'class': 'w-full file-input file-input-sm file-input-info',
                                                  'id': 'avatar'})
        self.fields['birthday'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                  'id': 'birthday'})
        self.fields['gender'].widget.attrs.update({'id': 'gender'})

        self.fields['password'].widget.attrs.update({'class': 'w-full input input-info input-sm',
                                                     'id': 'password'})

