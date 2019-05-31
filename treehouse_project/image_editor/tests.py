from django.test import TestCase

from user_profile.forms import PasswordChangeForm, UserProfileForm
from user_profile.models import UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.shortcuts import reverse



class ImageEditorViewTest(TestCase):
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
        self.image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg=="

        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.get(user=self.user)
        self.user_profile.first_name = 'miro'
        self.user_profile.last_name = 'hudec'
        self.user_profile.avatar = 'images/avatar.png'
        self.user_profile.save()

    def test_ImageEditor_edit(self):
        response = self.client.post(reverse('image_editor:edit'), data={
            'hidden': self.image
        })
        self.assertEqual(response.status_code, 302)

    def test_ImageEditor_edit_logout(self):
        self.client.logout()
        response = self.client.post(reverse('image_editor:edit'), data={
            'hidden': self.image
        })
        self.assertEqual(response.status_code, 302)

    def test_ImageEditor_get_edit(self):
        response = self.client.post(reverse('image_editor:edit'), {
            'hidden': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'image_editor/editor.html')
