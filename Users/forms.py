
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
        self.fields['username'].widget.attrs.update({'class': 'w-full input',
                                                     'id': 'username'})
        """self.fields['username']..widget.attrs.update({'class': 'text-white hover:ring-1 hover:ring-red-400 font-semibold'})"""
        self.fields['last_name'].widget.attrs.update({'class': 'w-full input',
                                                     'id': 'last_name'})
        self.fields['first_name'].widget.attrs.update({'class': 'w-full input',
                                                     'id': 'first_name'})
        self.fields['email'].widget.attrs.update({'class': 'w-full input',
                                                  'id': 'email'})
        self.fields['avatar'].widget.attrs.update({'class': 'w-full input',
                                                  'id': 'avatar'})
        self.fields['birthday'].widget.attrs.update({'class': 'w-full input',
                                                  'id': 'birthday'})
        self.fields['password'].widget.attrs.update({'class': 'w-full input',
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
        self.fields['username'].widget.attrs.update({'class': 'w-full input',
                                                     'id': 'username'})
        self.fields['password'].widget.attrs.update({'class': 'w-full input',
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
        self.fields['username'].widget.attrs.update({'class': 'input input-info text-slate-950  w-full',
                                                     'id': 'username'})
        self.fields['last_name'].widget.attrs.update({'class': 'w-full input input-info text-slate-950 ',
                                                     'id': 'last_name'})
        self.fields['first_name'].widget.attrs.update({'class': 'w-full input input-info text-slate-950 ',
                                                     'id': 'first_name'})
        self.fields['email'].widget.attrs.update({'class': 'w-full input input-info text-slate-950 ',
                                                  'id': 'email'})
        self.fields['avatar'].widget.attrs.update({'class': 'w-full file-input input-info text-slate-950 ',
                                                  'id': 'avatar'})
        self.fields['birthday'].widget.attrs.update({'class': 'w-full input input-info text-slate-950 ',
                                                  'id': 'birthday'})
        self.fields['gender'].widget.attrs.update({'id': 'gender'})

        self.fields['password'].widget.attrs.update({'class': 'w-full input input-info text-slate-950 ',
                                                     'id': 'password'})

