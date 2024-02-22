from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sender(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name: ', blank=False, null=False)
    email = models.EmailField(verbose_name='Email', blank=False, null=False)
    password = models.CharField(max_length=128, verbose_name='Password', blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders', verbose_name='User')

    class Meta:
        verbose_name_plural ="Senders"   

    def __str__(self):
        return self.name
    
