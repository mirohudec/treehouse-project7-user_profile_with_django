from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'image_editor'

urlpatterns = [
    path('', views.image_edit, name='edit')
]