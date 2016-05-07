from django.forms import TextInput
from django.forms.widgets import Textarea, CheckboxInput
from inventory.models import Object
from django.forms import ModelForm


class CreateObjectEntryForm(ModelForm):

    class Meta:
         model = Object
         fields = ['title', 'description', 'transport']
         widgets = {
             'title': TextInput({'class': 'form-control'}),
             'description': Textarea({'class': 'form-control'}),
             'transport': CheckboxInput({'class': 'checkbox-inline'})
         }