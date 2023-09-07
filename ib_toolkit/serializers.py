from rest_framework import serializers
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator
from .models import Datacenter


class CreateNetworkSerializer(serializers.Serializer):
    ENV_CHOICES = (
        ('dv', 'dv'),
        ('qa', 'qa'),
        ('pr', 'pr'),
    )
    DATACENTER_CHOICES = Datacenter.objects.values_list('name', flat=True).distinct()

    application_name = serializers.CharField(max_length=100)
    application_environment = serializers.ChoiceField(choices=ENV_CHOICES)
    cidr_size = serializers.IntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(31)]
    )
    datacenter = serializers.ChoiceField(choices=DATACENTER_CHOICES)


class GenericResposeSerializer(serializers.Serializer):
    status: serializers.BooleanField()
    message: serializers.CharField(max_length=200)
    details: serializers.DictField()