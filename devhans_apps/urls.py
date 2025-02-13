"""
URL configuration for devhans_apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls, name='dev_admin'),

    # core
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mailer/', include('mailer.urls')),
    path('raily/', include('raily_api.urls')),

    #apis
    path('api-auth/', include('rest_framework.urls')),
]
