from django.db import models
from django.contrib.auth.models import User
from django.core.validators import ValidationError

from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

import re


def bio_length_validator(value):
    # strip html tags
    clean = re.compile('<.*?>')
    string = re.sub(clean, '', value)
    # remove encoding
    string_two = string.replace('\ufeff', '')
    string_three = string_two.replace('&nbsp;', '')
    # remove space
    string_four = string_three.replace(' ', '')
    # count number of characters
    if len(string_four) < 10:
        raise ValidationError(
            'Bio has to be empty or at least 10 character or longer')


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile_of',
                                null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(validators=[bio_length_validator], blank=True)
    hobby = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'user_profile'


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """ Create blank user profile model when new user is created """
    UserProfile.objects.get_or_create(user=kwargs.get('instance'))


@receiver(post_init, sender=UserProfile)
def save_old_imagepath(sender, instance, **kwargs):
    """ Save the old image instance for removal"""
    # https://stackoverflow.com/questions/38232545/django-correctly-delete-image-after-updating-file
    if instance.avatar:
        instance._old_image = instance.avatar
    else:
        instance._old_image = False


@receiver(post_save, sender=UserProfile)
def delete_old_image(sender, instance, **kwargs):
    """ Remove old image file if changed"""
    if instance._old_image and instance._old_image != instance.avatar:
        instance._old_image.delete(save=False)
