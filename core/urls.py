from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.user_register, name='user_register'),
    path('profile/', views.profile, name='profile')
]