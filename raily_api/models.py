from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=1)
    tag = models.CharField(max_length=150, null=False, blank=False)
    origin = models.CharField(max_length=150, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    agent = models.CharField(max_length=200, null=False, blank=False)
    ip = models.CharField(max_length=20, null=False, blank=False)
    hostname = models.CharField(max_length=150, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    region = models.CharField(max_length=50, null=False, blank=False)
    loc = models.CharField(max_length=30, null=False, blank=False)
    org = models.CharField(max_length=150, null=False, blank=False)
    postal = models.CharField(max_length=10, null=False, blank=False)
    timezone = models.CharField(max_length=100, null=False, blank=False)


    class Meta:
        verbose_name_plural = "Visits"

    def __str__(self):
        return self.tag