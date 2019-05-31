from django.test import TestCase

from .forms import PasswordChangeForm, UserProfileForm
from .models import UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.shortcuts import reverse

# coverage run --source='.' manage.py test user_profile


class UserProfileModelTest(TestCase):
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

    def test_UserProfile_str(self):
        self.assertEqual(str(self.user_profile), 'miro hudec')

    def test_UserProfile_create_and_remove_images_signals(self):
        old_img = self.user_profile.avatar
        self.user_profile.avatar = 'images/new_avatar.jpg'
        self.user_profile.save()
        self.assertNotEqual(old_img, self.user_profile.avatar)


class UserProfileFormTest(TestCase):
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

    def test_UserProfileForm_valid(self):
        form = UserProfileForm(instance=self.user_profile, data={
            'first_name': 'miro',
            'last_name': 'hudec',
            'email': 'Miro.Hud@gmail.com',
            'confirm_email': 'Miro.Hud@gmail.com',
            'date_of_birth': '1991-06-28',
            'bio': '<p>no bio need just 10 letters</p>',
            'avatar': 'images/avatar.png',
        })

        self.assertTrue(form.is_valid())

    def test_UserProfileForm_invalid_confirm_email(self):
        form = UserProfileForm(instance=self.user_profile, data={
            'first_name': 'miro',
            'last_name': 'hudec',
            'email': 'Miro.Hud@gmail.com',
            'confirm_email': 'Miro.Hud@gmail.sk',
            'date_of_birth': '1991-06-28',
            'bio': '<p>no bio need just 10 letters</p>',
            'avatar': 'images/avatar.png',
        })

        self.assertEqual(
            form.errors['confirm_email'][0],
            'Email does not match')

    def test_UserProfileForm_invalid_bio(self):
        form = UserProfileForm(instance=self.user_profile, data={
            'first_name': 'miro',
            'last_name': 'hudec',
            'email': 'Miro.Hud@gmail.com',
            'confirm_email': 'Miro.Hud@gmail.com',
            'date_of_birth': '1991-06-28',
            'bio': '<p>no bio need </p>',
            'avatar': 'images/avatar.png',
        })

        self.assertEqual(
            form.errors['bio'][0],
            'Bio has to be empty or at least 10 character or longer')

    def test_UserProfileForm_invalid_date_format(self):
        form = UserProfileForm(instance=self.user_profile, data={
            'first_name': 'miro',
            'last_name': 'hudec',
            'email': 'Miro.Hud@gmail.com',
            'confirm_email': 'Miro.Hud@gmail.com',
            'date_of_birth': '28/06/1991',
            'bio': '<p>no bio need just 10 letters</p>',
            'avatar': 'images/avatar.png',
        })

        self.assertEqual(
            form.errors['date_of_birth'][0],
            'Enter a valid date.')


class PasswordChangeFormTest(TestCase):

    def setUp(self):
        form = UserCreationForm(data={
            'username': 'miro',
            'password1': 'Qwertyuiop164964+',
            'password2': 'Qwertyuiop164964+'
        })
        form.save()
        self.user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        self.old_pw = 'Qwertyuiop164964+'
        self.new_pw = 'Qwertyuiop164964-'

    def test_PasswordChangeForm_valid(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password': self.new_pw,
            'confirm_password': self.new_pw
        }, user=self.user)
        self.assertTrue(form.is_valid())

    def test_PasswordChangeForm_missing_special_character(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password': self.new_pw.replace('-', 'l'),
            'confirm_password': self.new_pw.replace('-', 'l'),
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['new_password'][0],
            'New password must include special characters, such as @, #, $')

    def test_PasswordChangeForm_missing_number(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password': self.new_pw.replace('164964', 'hhhhhh'),
            'confirm_password': self.new_pw.replace('164964', 'hhhhhh'),
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['new_password'][0],
            'New password must include one or more digits')

    def test_PasswordChangeForm_missing_upper_or_lower(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password': self.new_pw.replace('Q', 'q'),
            'confirm_password': self.new_pw.replace('Q', 'q'),
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['new_password'][0],
            'New password must include both upper and lower characters')

    def test_PasswordChangeForm_not_the_same(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password': self.new_pw.replace('Q', 'q'),
            'confirm_password': self.new_pw.replace('Q', 'r'),
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['new_password'][0],
            'Passwords do not match')

    def test_PasswordChangeForm_not_the_same_as_old(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password': self.old_pw,
            'confirm_password': self.old_pw
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['new_password'][0],
            'Passwords must be different')

    def test_PasswordChangeForm_incorrect_password(self):
        form = PasswordChangeForm(data={
            'current_password': self.new_pw,
            'new_password': self.new_pw,
            'confirm_password': self.new_pw
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['current_password'][0],
            'Password incorrect')

    def test_PasswordChangeForm_not_similar(self):
        form = PasswordChangeForm(data={
            'current_password': self.old_pw,
            'new_password':  'Miromiromiro1+',
            'confirm_password': 'Miromiromiro1+'
        }, user=self.user)
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['new_password'][0],
            'The password is too similar to the username.')


class UserProfileViewsTests(TestCase):
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
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.first_name = 'miro'
        self.user_profile.last_name = 'hudec'
        self.user_profile.avatar = 'images/avatar.png'
        self.user_profile.save()
        self.instance = self.user_profile

    def test_UserProfile_home(self):
        response = self.client.get(reverse('user_profile:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile_home.html')
        self.assertEqual(response.context['user_data'].first_name, 'miro')

        self.assertEqual(response.context['user_data'].last_name, 'hudec')

    def test_UserProfile_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('user_profile:home'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/sign_in/')

    def test_UserProfile_get_edit(self):
        response = self.client.get(reverse('user_profile:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile_edit.html')

    def test_UserProfile_post_edit_success(self):
        response = self.client.post(reverse('user_profile:edit'), data={
            'first_name': 'miroslav',
            'last_name': 'hudec',
            'email': 'Miro.Hud@gmail.com',
            'confirm_email': 'Miro.Hud@gmail.com',
            'date_of_birth': '1991-06-28',
            'bio': '<p>no bio need just 10 letters or longer</p>',
            'avatar': 'images/avatar2.png',
        })
        self.assertEqual(response.status_code, 302)

    def test_UserProfile_post_edit_fail(self):
        with self.assertRaises(KeyError):
            self.client.post(reverse('user_profile:edit'), data={
                'first_name': 'miroslav',
                'last_name': 'hudec',
                'email': 'Miro.Hudgmail.com',
                'confirm_email': 'Miro.Hud@gmail.com',
                'date_of_birth': '1991-06-28',
                'bio': '<p>no bio need just 10 letters or longer</p>',
                'avatar': 'images/avatar3.png',
            })

    def test_UserProfile_edit_logout(self):
        self.client.logout()
        response = self.client.get(reverse('user_profile:edit'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/sign_in/')

    def test_UserProfile_change_password_success(self):
        response = self.client.post(reverse('user_profile:change_password'),
                                    data={
            'current_password': 'Qwertyuiop164964+',
            'new_password': 'Qwertyuiop164964-',
            'confirm_password': 'Qwertyuiop164964-'
        })
        self.assertEqual(response.status_code, 302)
        self.user = User.objects.get(username='miro')
        # password shoul be different
        self.assertFalse(self.user.check_password('Qwertyuiop164964+'))
        self.assertTrue(self.user.check_password('Qwertyuiop164964-'))

    def test_UserProfile_change_password_fail(self):
        response = self.client.post(reverse('user_profile:change_password'),
                                    data={
            'current_password': 'Qwertyuiop164964+',
            'new_password': 'Qwertyuiop164964-',
            'confirm_password': 'Qwertyuiop164964--'
        })
        self.assertEqual(response.status_code, 200)
        self.user = User.objects.get(username='miro')
        # should be the same password
        self.assertTrue(self.user.check_password('Qwertyuiop164964+'))

    def test_UserProfile_change_password_logout(self):
        self.client.logout()
        response = self.client.get(reverse('user_profile:change_password'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/sign_in/')
