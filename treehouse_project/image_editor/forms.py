from django import forms


class ImageUploadForm(forms.Form):
    hidden = forms.CharField(required=False, widget=forms.HiddenInput)
