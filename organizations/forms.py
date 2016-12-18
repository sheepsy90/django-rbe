from django import forms

from organizations.models import OrganizationDescription


class OrganizationDescriptionForm(forms.ModelForm):

    class Meta:
        model = OrganizationDescription
        exclude = ['organization']
        widgets = {
            'summary': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize: none'}),
            'value_system': forms.Textarea(attrs={'class': 'form-control'}),
            'decision_making': forms.Textarea(attrs={'class': 'form-control'}),
            'when_join': forms.Textarea(attrs={'class': 'form-control'})
        }