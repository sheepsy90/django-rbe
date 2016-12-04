from django import forms

from location.constants import COUNTRIES
from location.models import LOCATION_PRECISION


class LocationDetailsForm(forms.Form):
    longitude = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Longitude',
                                max_length=64, required=False, help_text="The longitude in the format +/- XX.YYYYYY")

    latitude = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Latitude', max_length=64,
                               required=False, help_text="The latitude in the format +/- XX.YYYYYY")

    location_precision = forms.CharField(
        widget=forms.Select(choices=LOCATION_PRECISION, attrs={'class': 'form-control'}), label='Location Precision',
        help_text="Whether or not you want to show your location precisely to other people.")

    location_trace = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                                     label='Location Traceback', required=False)

    country = forms.CharField(widget=forms.Select(choices=COUNTRIES, attrs={'class': 'form-control'}), label='Country',
                              max_length=256, required=False, help_text="The country you live in")

    @property
    def has_location(self):
        long, lat = self.longlat_value
        return long and lat

    @property
    def longlat_value(self):
        longitude = self.cleaned_data['longitude']
        latitude = self.cleaned_data['latitude']
        return longitude, latitude

    def clean(self):
        cleaned_data = super(LocationDetailsForm, self).clean()

        longitude = cleaned_data['longitude']
        latitude = cleaned_data['latitude']

        # If both are not set that is fine - meaning no location
        if latitude or longitude:
            # First parse the latitude and longitude

            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except:
                forms.ValidationError("Longitude/Latitude not correct")

            if not (-90 <= latitude <= 90) or not(-180 <= longitude < 180):
                raise forms.ValidationError("Longitude/Latitude not correct")
