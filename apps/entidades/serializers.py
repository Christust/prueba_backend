from rest_framework import serializers
from apps.entidades import models


class MaestroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Maestro
        exclude = []


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salon
        exclude = []
