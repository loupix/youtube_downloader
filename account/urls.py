from django.urls import include, path, re_path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
]