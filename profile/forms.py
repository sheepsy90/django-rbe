from django import forms
from django.forms import ModelForm

from profile.models import InvitationKey


class InviteForm(ModelForm):
    class Meta:
        model = InvitationKey
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
