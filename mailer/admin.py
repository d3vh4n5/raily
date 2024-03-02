from django.contrib import admin
from .models import ApiKey, Sender

# Register your models here.

admin.site.register(ApiKey)
admin.site.register(Sender)