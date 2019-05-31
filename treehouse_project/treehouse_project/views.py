from django.shortcuts import render

from user_profile.models import UserProfile


def home(request):
    return render(request, 'home.html')
