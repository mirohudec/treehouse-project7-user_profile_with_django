from django import forms
from password_strength_field.widgets import PasswordStrengthMeter

from .models import UserProfile

from django.core.validators import ValidationError
from django.contrib.auth.password_validation import validate_password

from django_summernote.widgets import SummernoteWidget
from bootstrap_datepicker_plus import DatePickerInput


class UserProfileForm(forms.ModelForm):

    date_of_birth = forms.DateField(required=False,
                                    widget=DatePickerInput(format='%Y-%m-%d'))
    bio = forms.CharField(
        widget=SummernoteWidget(
            attrs={'summernote': {'cols': 80, 'rows': 10}}), required=False)
    confirm_email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'date_of_birth',
            'state',
            'city',
            'hobby',
            'bio',
            'avatar'
        ]

    def __init__(self, *args, **kwargs):
        # if email exist populate confirm email field
        self.email = kwargs['instance'].email
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
    confirm_password = forms.CharField(
        widget=PasswordStrengthMeter)

    def __init__(self, *args, **kwargs):
        # make PasswordChangeForm take user argument
        self.user = kwargs.pop('user')
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data['current_password']
        password_one = cleaned_data['new_password']
        password_two = cleaned_data['confirm_password']

        new_pw = True

        if self.user.check_password(current_password):
            try:
                validate_password(password_one, self.user)
            except ValidationError as e:
                self.add_error('new_password', e)
                new_pw = False
            if password_one != password_two:
                self.add_error('new_password', 'Passwords do not match')
                new_pw = False
            if password_one == current_password:
                self.add_error('new_password',
                               'Passwords must be different')
                new_pw = False
            if check_lower_uppercase(password_one):
                self.add_error(
                    'new_password',
                    'New password must include both ' +
                    'upper and lower characters')
                new_pw = False
            if check_number(password_one):
                self.add_error('new_password',
                               'New password must include one or more digits')
                new_pw = False
            if check_special_characters(password_one):
                self.add_error(
                    'new_password',
                    'New password must include special ' +
                    'characters, such as @, #, $')
                new_pw = False
            if new_pw:
                self.user.set_password(password_one)
                self.user.save()
        else:
            self.add_error('current_password', 'Password incorrect')

        return cleaned_data


def check_lower_uppercase(password):
    lower = False
    upper = False
    for c in password:
        if c.islower():
            lower = True
        if c.isupper():
            upper = True
        if upper and lower:
            break
    if lower is False or upper is False:
        return True
    return False


def check_number(password):
    for c in password:
        if c in '0123456789':
            return False
    return True


def check_special_characters(password):
    for c in password:
        # https://www.owasp.org/index.php/Password_special_characters
        if c in "$%&'()*+,-./:;<=>?@[\\]^_`{|}~":
            return False
    return True
