from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='mailer'),
    path('create_sender/', views.create_sender, name='create_sender'),
    path('sender_detail/<int:pk>', views.sender_detail, name='sender_detail'),
    path('senders_list/', views.senders_list, name='senders_list'),
]