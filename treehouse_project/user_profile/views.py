from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import UserProfileForm, PasswordChangeForm


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
    form = UserProfileForm(instance=user_data)
    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_data)
        if form.is_valid():
            profile = form.save(commit=False)
            user = User.objects.get(id=profile.user_id)
            user.first_name = profile.first_name
            user.last_name = profile.last_name
            user.email = profile.email
            profile.save()
            user.save()
            messages.success(request, 'Successfuly updated the profile!')
            return redirect('user_profile:home')
    return render(request, 'user_profile/profile_edit.html', {'form': form})


def profile_change_password(request):
    if not request.user.is_authenticated:
        return redirect('accounts:sign_in')
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            update_session_auth_hash(request, request.user)
            return redirect('user_profile:home')
    return render(request,
                  'user_profile/profile_change_password.html', {'form': form})
