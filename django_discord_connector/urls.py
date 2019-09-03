from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('sso/callback', views.sso_callback,
         name="django-discord-connector-sso-callback"),
    path('sso/token/add/', views.add_sso_token,
         name="django-discord-connector-sso-token-add"),
    path('sso/token/remove/<int:pk>/', views.remove_sso_token,
         name="django-discord-connector-sso-token-remove"),
]
