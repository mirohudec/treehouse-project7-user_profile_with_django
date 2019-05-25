from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import update_session_auth_hash

from .models import UserProfile
from .forms import UserProfileForm, PasswordChangeForm


thumbnail_size = 256, 256


def profile_home(request):
    if not request.user.is_authenticated:
        return redirect('accounts:sign_in')
    user_data = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile/profile_home.html',
                  {'user_data': user_data})


def profile_edit(request):
    if not request.user.is_authenticated:
        return redirect('accounts:sign_in')
    user_data = UserProfile.objects.get(user=request.user)
    form = UserProfileForm(instance=user_data, email=request.user.email)
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_data, email=request.user.email)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            # image = Image.open(
            #     f'{settings.MEDIA_ROOT}{user_data.avatar}')
            # image.thumbnail(thumbnail_size)
            # image.save(
            #     f'{settings.MEDIA_ROOT}' +
            #     f'{user_data.avatar}.thumbnail.jpeg', 'JPEG')
            messages.success(request, 'Successfuly updated the profile!')
            return redirect('user_profile:home')
    return render(request, 'user_profile/profile_edit.html', {'form': form})


def profile_change_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            update_session_auth_hash(request, request.user)
            return redirect('user_profile:home')
    return render(request,
                  'user_profile/profile_change_password.html', {'form': form})
