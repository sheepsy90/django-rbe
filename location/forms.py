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

        if latitude or longitude:
        # First parse the latitude and longitude
            try:
                self.validate_longlat(latitude, longitude)
            except ValueError as ve:
                raise forms.ValidationError(ve.message)
            except Exception:
                raise forms.ValidationError("Could not validate form")

    @staticmethod
    def validate_longlat(latitude, longitude):
        # If both are not set that is fine - meaning no location
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except:
            ValueError("Longitude/Latitude not correct")

        if not (-90 <= latitude <= 90) or not (-180 <= longitude < 180):
            raise ValueError("Longitude/Latitude not correct")
