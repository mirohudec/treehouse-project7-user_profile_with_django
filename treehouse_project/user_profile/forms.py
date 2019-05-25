from django import forms
from django.http import request

from .models import UserProfile

from django.contrib.auth.models import User

from django_summernote.widgets import SummernoteWidget
from bootstrap_datepicker_plus import DatePickerInput


class UserProfileForm(forms.ModelForm):

    date_of_birth = forms.DateField(required=False,
                                    widget=DatePickerInput(format='%Y-%m-%d'))
    bio = forms.CharField(
        widget=SummernoteWidget(
            attrs={'summernote': {'cols': 80, 'rows': 10}}), required=False)
    confirm_email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'date_of_birth',
            'bio',
            'avatar'
        ]

    def __init__(self, *args, **kwargs):
        # pass email fropm logged in user and set initial value for confirm email
        self.email = kwargs.pop('email')
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.email:
            self.fields['confirm_email'].initial = self.email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        confirm_email = cleaned_data['confirm_email']

        if email != confirm_email:
            self.add_error('confirm_email', 'Email does not match')

        return cleaned_data


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        # make PasswordChangeForm take user argument
        self.user = kwargs.pop('user')
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data['current_password']
        password_one = cleaned_data['new_password']
        password_two = cleaned_data['confirm_password']

        if self.user.check_password(current_password):
            if password_one != password_two:
                self.add_error('confirm_password', 'Passwords do not match')
            else:
                self.user.set_password(password_one)
                self.user.save()
        else:
            self.add_error('current_password', 'Password incorrect')

        return cleaned_data
