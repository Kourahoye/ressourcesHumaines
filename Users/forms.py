
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
        self.fields['username'].widget.attrs.update({'class': 'w-full input input-info input-sm dark:text-white',
                                                     'id': 'username'})
        self.fields['password'].widget.attrs.update({'class': 'w-full input input-info input-sm dark:text-white',
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





# accounts/forms.py
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from .models import User  # ton CustomUser

class CustomPasswordChangeForm(forms.Form):

    old_password = forms.CharField(
        label="Mot de passe actuel",
        widget=forms.PasswordInput(attrs={'class': 'w-full input input-info input-sm'})
    )
    new_password1 = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'w-full input input-info input-sm'}),
        # help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label="Confirmer le nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'w-full input input-info input-sm'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # obligatoire
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not check_password(old_password, self.user.password):
            raise forms.ValidationError("Le mot de passe actuel est incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "Les mots de passe ne correspondent pas.")
        return cleaned_data

        # Validation des règles Django
        # if new_password1:
        #     try:
        #         password_validation.validate_password(new_password1, self.user)
        #     except forms.ValidationError as e:
        #         self.add_error('new_password1', e)
        # return cleaned_data

    # def save(self, commit=True):
    #     password = self.cleaned_data["new_password1"]
    #     self.user.set_password(password)
    #     if hasattr(self.user, 'must_change_password'):
    #         self.user.must_change_password = False
    #     if commit:
    #         self.user.save()
    #     return self.user
