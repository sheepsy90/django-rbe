from django import forms



class ProfileDetailsForm(forms.Form):
    about_me_text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}),
                                    label='About', max_length=3000, required=False)

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label='First name', max_length=64, required=False)

    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='Last name', max_length=64, required=False)

    profile_email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                   'readonly': 'readonly'}),
                                    label='Email', max_length=100)
