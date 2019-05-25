from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.profile_home, name='home'),
    path('edit/', views.profile_edit, name='edit'),
    path('change_password/', views.profile_change_password, name='change_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
