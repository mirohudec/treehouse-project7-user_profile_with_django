from django.test import TestCase

from user_profile.forms import PasswordChangeForm, UserProfileForm
from user_profile.models import UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.shortcuts import reverse


class AccountsViewsTest(TestCase):
    def setUp(self):
        form = UserCreationForm(data={
            'id': 10,
            'username': 'miro',
            'password1': 'Qwertyuiop164964+',
            'password2': 'Qwertyuiop164964+'
        })
        form.save()
        self.user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.first_name = 'miro'
        self.user_profile.last_name = 'hudec'
        self.user_profile.avatar = 'images/avatar.png'
        self.user_profile.save()

    def test_sing_in_success(self):
        response = self.client.post(reverse('accounts:sign_in'), data={
            'username': 'miro',
            'password': 'Qwertyuiop164964+'
        })
        self.assertEqual(response.status_code, 302)

    def test_sing_in_fail(self):
        response = self.client.post(reverse('accounts:sign_in'), data={
            'username': 'miro',
            'password': 'Qwerty'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Please enter a correct username and password')

    def test_sing_up_success(self):
        response = self.client.post(reverse('accounts:sign_in'), data={
            'username': 'miro',
            'password': 'Qwertyuiop164964+'
        })
        self.assertEqual(response.status_code, 302)
