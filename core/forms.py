from core.models import RegistrationKey
from django import forms
from django.contrib.auth.models import User
from django.forms import Form
from django.forms.models import ModelForm
from django.forms.widgets import PasswordInput, EmailInput, TextInput
from django.conf import settings


class RegistrationForm(Form):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=EmailInput(attrs={'class': 'form-control'}),
                            help_text="Select an email address that you can confirm (feature not enabled yet)!")

    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))
    password_repeat = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}),
                                      help_text="Choose a strong password")

    registration_key = forms.CharField(max_length=64, required=True, widget=TextInput(attrs={'class': 'form-control'}),
                                       help_text="Put in the registration key.")

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        email = cleaned_data.get("email")
        registration_key = cleaned_data.get("registration_key")

        username = cleaned_data.get("username")

        validation_errors = {}

        if User.objects.filter(username=username).exists():
            validation_errors.update({'username': "Sorry this username is already taken!"})

        if User.objects.filter(email=email).exists():
            validation_errors.update({'email': "Sorry this email is already taken!"})

        if password and password_repeat:
            # Only do something if both fields are valid so far.
            if password != password_repeat:
                validation_errors.update({'password_repeat': "Passwords don't match!"})

        if settings.CLOSED_NETWORK:
            if not RegistrationKey.objects.filter(key=registration_key).exists():
                validation_errors.update({'registration_key': "The registration key is not valid!"})

        if validation_errors:
            raise forms.ValidationError(validation_errors)


class LoginForm(Form):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}))


class InviteForm(ModelForm):
    class Meta:
        model = RegistrationKey
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class PasswordChangeForm(Form):
    old_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}), help_text="Enter your old password!")
    new_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}), help_text="Enter a new password!")
    repeat_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}), help_text="Repeat the new password for typo checking!")

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data.get("new_password")
        password_repeat = cleaned_data.get("repeat_password")

        if password != password_repeat:
            raise forms.ValidationError({'new_password': "Passwords do not match!"})


class PasswordReset(Form):
    key = forms.CharField(widget=TextInput(attrs={'style': 'display: none;'}))
    new_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}), help_text="Enter a new password!")
    repeat_password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control'}), help_text="Repeat the new password for typo checking!")

    def clean(self):
        cleaned_data = super(PasswordReset, self).clean()
        password = cleaned_data.get("new_password")
        password_repeat = cleaned_data.get("repeat_password")

        if password != password_repeat:
            raise forms.ValidationError({'new_password': "Passwords do not match!"})


class PasswordResetRequest(Form):

    email = forms.CharField(widget=EmailInput(attrs={'class': 'form-control'}),
                            help_text="Please enter your email address!")

    def clean(self):
        cleaned_data = super(PasswordResetRequest, self).clean()
        email = cleaned_data.get("email")

        if not email or len(email) < 6:
            raise forms.ValidationError({'email': "Please enter an email address!"})
