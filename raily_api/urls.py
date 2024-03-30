from django.urls import re_path
from . import views

urlpatterns = [
    re_path('api/add_visit', views.add_visit)
]
