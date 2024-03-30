from rest_framework import serializers
from .models import Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Visit
        # fields = ['id', 'username', 'password', 'email']
        fields = ["__all__"]