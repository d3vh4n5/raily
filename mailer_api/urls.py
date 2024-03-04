from django.urls import re_path
from . import views

urlpatterns = [
    re_path('login', views.login),
    re_path('signup', views.signup),
    re_path('test_token', views.test_token),
    re_path('custom_mail_send', views.custom_mail_send),
    re_path('server_mail_send', views.server_mail_send),
]
