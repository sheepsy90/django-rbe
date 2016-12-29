import requests
from django import forms
from django.core.exceptions import ValidationError

from organizations.models import OrganizationDescription, OrganizationPost, Organization


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


class OrganizationCreateForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Name',
                           max_length=64, required=True, help_text="Please enter a name for your organisation")

    website = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Website URL',
                             max_length=256, required=True,
                             help_text="Please enter a website url for further information")

    contact_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Contact email',
                                     max_length=256, required=True,
                                     help_text="Please enter a email for further questions")

    def clean_name(self):
        name = self.cleaned_data['name']
        if Organization.objects.filter(name=name).exists():
            raise ValidationError('Organization name is already taken!')
        return name

    def clean_website(self):
        website = self.cleaned_data['website']

        try:
            response = requests.get(website)
            assert response.status_code in [200, 302]
        except Exception as e:
            raise ValidationError('Could not reach website - make sure it is correct!')

        return website


class OrganizationPostForm(forms.ModelForm):
    class Meta:
        model = OrganizationPost
        exclude = ['organization', 'created', 'author']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize: none'})
        }
