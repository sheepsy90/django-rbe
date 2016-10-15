from django import forms
from django.forms import Form
from django.forms.widgets import Textarea, TextInput, HiddenInput


class ComposeForm(Form):
    recipient_id = forms.CharField(widget=HiddenInput(attrs={'class': 'form-control'}))
    recipient_name = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    subject = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'maxlength': '120'}))
    body = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'style': 'resiye: none', 'rows': '10', 'maxlength': '1200'}))
