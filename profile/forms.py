from django import forms
from django.forms import ModelForm

#from profile.models import RegistrationKey
from core.models import RegistrationKey


class InviteForm(ModelForm):
    class Meta:
        model = RegistrationKey
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
