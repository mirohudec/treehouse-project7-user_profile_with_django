from django import forms
from django.http import request


class ImageUploadForm(forms.Form):
    hidden = forms.CharField(widget=forms.HiddenInput)
