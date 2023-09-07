# Generated by Django 4.2.4 on 2023-08-05 03:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datacenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_character', message='Only alphanumeric characters and underscores are allowed.', regex='^[a-zA-Z0-9_]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='DatacenterNetworkBlock',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('child_network_size', models.IntegerField(validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(16)])),
                ('container_network', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(code='invalid_cidr', message='Enter a valid CIDR notation (e.g., 192.168.0.0/24).', regex='^(\\d{1,3}\\.){3}\\d{1,3}/\\d{1,2}$')])),
                ('datacenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='networks', to='ib_toolkit.datacenter')),
            ],
        ),
    ]