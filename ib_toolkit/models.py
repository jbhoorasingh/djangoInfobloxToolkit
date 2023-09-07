from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
import uuid
from .utils import alphanumeric_and_underscore_validator, cidr_validator


class Datacenter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=10, validators=[alphanumeric_and_underscore_validator])

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Datacenter, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class DatacenterNetworkBlock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child_network_size = models.IntegerField(null=False, validators=[MaxValueValidator(31), MinValueValidator(16)])
    container_network = models.CharField(null=False, max_length=20, validators=[cidr_validator])
    datacenter = models.ForeignKey(Datacenter, on_delete=models.CASCADE, related_name='networks')

    class Meta:
        verbose_name = 'Datacenter Network Block'
        verbose_name_plural = 'Datacenter Network Blocks'

    def __str__(self):
        return f'{self.datacenter.name} - /{self.child_network_size} - {self.container_network}'


class Network(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.CharField(max_length=50, null=False)
    application_environment = models.CharField(max_length=5, null=False)
    datacenter_name = models.CharField(max_length=10, )
    network = models.CharField(null=False, max_length=20, validators=[cidr_validator])
    infoblox_ref = models.CharField(max_length=255, null=False)
    created_by = models.CharField(max_length=50, validators=[alphanumeric_and_underscore_validator])





